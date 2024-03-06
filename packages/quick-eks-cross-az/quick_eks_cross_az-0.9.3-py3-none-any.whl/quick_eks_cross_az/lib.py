import collections
import csv
import json
import os
from contextlib import contextmanager
from io import StringIO
from time import sleep

import boto3
import botocore
import yaml
from botocore.exceptions import ClientError
from kubernetes import client, config
from yaspin import yaspin
from yaspin.spinners import Spinners


@contextmanager
def spinner(*args, **kwds):
    with yaspin(Spinners.line, *args, **kwds) as sp:
        yield sp


class CrossAzLogger:
    def __init__(
        self,
        accumulation_minutes=5,
        verbose=False,
        output_file_name="./cross-az.csv",
        cf_stack_name="quick-eks-cross-az",
    ) -> None:
        self.accumulation_minutes = accumulation_minutes
        self.verbose = verbose
        self.output_file_name = output_file_name
        self.cf_stack_name = cf_stack_name

        self.kube_client = None
        self.cloudformation_client = None
        self.eks_client = None

    def setup_clients(self):
        self.kub_config = config.load_kube_config()
        self.kube_client = client.CoreV1Api()

        self.cloudformation_client = boto3.client("cloudformation")
        self.eks_client = boto3.client("eks")
        self.ec2_client = boto3.client("ec2")
        self.athena_client = boto3.client("athena")
        self.s3_client = boto3.client("s3")

    def log(self, s, is_debug=False):
        if is_debug and not self.verbose:
            return
        print(s)

    def get_cloudformation(self):
        self.log("getting cloudformation specs...", is_debug=True)
        script_dir = os.path.dirname(__file__)
        cf_filepath = os.path.join(script_dir, "./cloudformation.yaml")
        with open(cf_filepath, "r") as fin:
            stack = yaml.safe_load(fin)
        del stack["Parameters"]["BootstrapVersion"]
        del stack["Rules"]
        return stack

    def get_query_sql(self):
        self.log("Loading Athena query from file...", is_debug=True)
        script_dir = os.path.dirname(__file__)
        cf_filepath = os.path.join(script_dir, "./query.sql")
        with open(cf_filepath, "r") as fin:
            sql = fin.read()
        return sql

    def get_pods_mapping(self):
        self.log("Gathering Kubernetes cluster data...", is_debug=True)
        AZ_LABEL = "topology.kubernetes.io/zone"
        TIME_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

        nodes_azs = {}

        self.log("Retrieving node list...", is_debug=True)
        nodes = self.kube_client.list_node(watch=False)

        for node in nodes.items:
            nodes_azs[node.metadata.name] = (
                node.metadata.labels[AZ_LABEL] if AZ_LABEL in node.metadata.labels else "<none>"
            )
        self.log(f"Retrieved {len(nodes.items)} nodes", is_debug=True)

        pods_info = []

        self.log("Retrieving pods list...", is_debug=True)
        pods = self.kube_client.list_pod_for_all_namespaces(label_selector="app", watch=False)
        self.log(f"Retrieved {len(pods.items)} pods", is_debug=True)
        for pod in pods.items:
            conditions = pod.status.conditions
            ready_condition = next(filter(lambda cond: cond.type == "Ready", conditions))
            pod_creation_time = ready_condition.last_transition_time.strftime(TIME_DATE_FORMAT)

            info = {
                "name": pod.metadata.name,
                "ip": pod.status.pod_ip,
                "app": pod.metadata.labels.get("app", "<none>"),
                "creation_time": pod_creation_time,
                "node": pod.spec.node_name,
                "az": nodes_azs.get(pod.spec.node_name, "<none>"),
            }

            pods_info.append(info)
        return pods_info

    def get_cluster_name_from_kube_context(self):
        _, current_context = config.list_kube_config_contexts()

        cluster_arn = current_context["context"]["cluster"]
        cluster_name = cluster_arn.split("/")[-1]
        return cluster_name

    def get_eks_cluster_vpc_id(self, cluster_name):
        cluster = self.eks_client.describe_cluster(name=cluster_name)

        vpc_id = cluster["cluster"]["resourcesVpcConfig"]["vpcId"]
        return vpc_id

    def test_credentials(self):
        try:
            _pods = self.get_pods_mapping()
        except Exception as e:
            self.log(f"could not get pods from current kube context: {e}")
            return False

        try:
            cluster_name = self.get_cluster_name_from_kube_context()
        except Exception as e:
            self.log(f"could not get EKS cluster name from current kube context: {e}")
            return False

        try:
            vpc_id = self.get_eks_cluster_vpc_id(cluster_name)
            _flow_logs = self.ec2_client.describe_flow_logs(
                Filter=[
                    {
                        "Name": "resource-id",
                        "Values": [
                            vpc_id,
                        ],
                    }
                ]
            )
        except Exception as e:
            self.log(f"could not list flow logs from EKS cluster: {e}")
            return False

        return True

    def get_stack_logical_mapping(self, stack_name):
        resources = self.cloudformation_client.describe_stack_resources(StackName=stack_name)
        return {r["LogicalResourceId"]: r["PhysicalResourceId"] for r in resources["StackResources"]}

    def upload_pod_ips(self, bucket_name):
        mapping = self.get_pods_mapping()
        self.log("Uploading pod mapping data...", is_debug=True)
        buffer = StringIO()
        headers = list(mapping[0].keys())
        writer = csv.writer(buffer)
        writer.writerow(headers)
        for pod in mapping:
            writer.writerow([pod[h] for h in headers])
        self.s3_client.put_object(Body=buffer.getvalue(), Bucket=bucket_name, Key="pods_metadata.csv")

    def run(self):
        try:
            cf = self.get_cloudformation()
            cluster_name = self.get_cluster_name_from_kube_context()
            vpc_id = self.get_eks_cluster_vpc_id(cluster_name)

            with spinner(text="Creating CloudFormation stack for flow logs and S3 buckets...") as sp:
                self.deploy_cf_stack(cf, self.cf_stack_name, {"eksVpcId": vpc_id})
                sp.ok()

            logical_physical_mapping = self.get_stack_logical_mapping(self.cf_stack_name)

            self.upload_pod_ips(logical_physical_mapping["podstatebucket582E33CB"])

            self.log(f"accumulating {self.accumulation_minutes} minutes of flow log data... (Ctrl+C to stop early)")
            with spinner(text="elapsed time", timer=True) as sp:
                try:
                    sleep(self.accumulation_minutes * 60)
                except KeyboardInterrupt as _e:
                    self.log("early keyboard interruption")
                sp.ok()

            with spinner(text="Aggregating data in Athena...") as sp:
                self.run_athena_query_to_csv(
                    logical_physical_mapping["AthenaAnalyzerpodstableTable59EBB00B"],
                    logical_physical_mapping["AthenaAnalyzerflowlogstableTableD01608E8"],
                    logical_physical_mapping["AthenaAnalyzerathenaresults88B510AC"],
                    self.output_file_name,
                )
                sp.ok()

            self.print_summary(self.output_file_name)

            with spinner(text="Cleaning up deployment...") as sp:
                self.cleanup_and_delete_cf_stack(self.cf_stack_name)
                sp.ok()

        except KeyboardInterrupt as _e:
            self.log("keyboard interruption. aborting and trying to clean up...")
            self.cleanup_and_delete_cf_stack(self.cf_stack_name)

        except Exception as e:
            self.log(f"exception while accumulating flow logs: {e}")

            self.log("Cleaning up deployment...")
            self.cleanup_and_delete_cf_stack(self.cf_stack_name)

    def wait_for_athena_query(self, query_execution_id):
        query_status = "RUNNING"

        while query_status == "RUNNING":
            try:
                status_response = self.athena_client.get_query_execution(QueryExecutionId=query_execution_id)

                query_status = status_response["QueryExecution"]["Status"]["State"]

                if query_status == "FAILED":
                    raise Exception(
                        "Athena query failed to run with error: "
                        + status_response["QueryExecution"]["Status"]["StateChangeReason"]
                    )

                elif query_status == "SUCCEEDED":
                    return
            except botocore.errorfactory.InvalidRequestException as e:
                if "Query has not yet finished" in str(e):
                    sleep(3)
                    continue
            sleep(3)

    def get_named_queries_ids_in_stack(self, stack_name):
        resources = self.cloudformation_client.describe_stack_resources(StackName=stack_name)
        return [
            x["PhysicalResourceId"]
            for x in resources["StackResources"]
            if x.get("ResourceType") == "AWS::Athena::NamedQuery"
        ]

    def run_athena_query_to_csv(self, pods_table_name, vpc_flow_logs_table_name, result_bucket, csv_path):
        query_string = self.get_query_sql().format(
            pods_table_name=pods_table_name,
            vpc_flow_logs_table_name=vpc_flow_logs_table_name,
            invokation_frequency="",
        )
        response = self.athena_client.start_query_execution(
            QueryString=query_string,
            ResultConfiguration={"OutputLocation": f"s3://{result_bucket}/"},
            QueryExecutionContext={"Database": "eks-inter-az-visibility"},
        )

        query_execution_id = response["QueryExecutionId"]

        self.wait_for_athena_query(query_execution_id)

        _results_response = self.athena_client.get_query_results(QueryExecutionId=query_execution_id)
        # results_response['ResponseMetadata']['RequestId']

        my_bucket = boto3.resource("s3").Bucket(result_bucket)
        my_bucket.download_file(query_execution_id + ".csv", csv_path)

    def cleanup_and_delete_cf_stack(self, stack_name):
        """
        removes everything but buckets, empties them, then removes them too
        """
        if not self.is_stack_exists(stack_name):
            self.log("stack does not exist, nothing to cleanup")
            return

        only_buckets = self.get_only_buckets_template_from_cloudformation(stack_name)
        self.deploy_cf_stack(only_buckets, stack_name, {"eksVpcId": ""})

        resources = self.cloudformation_client.describe_stack_resources(StackName=stack_name)
        buckets = [x["PhysicalResourceId"] for x in resources["StackResources"]]
        for bucket in buckets:
            if self.bucket_exists(bucket):
                self.empty_bucket(bucket)

        self.cloudformation_client.delete_stack(StackName=stack_name)

    def bucket_exists(self, bucket_name):
        try:
            _resp = self.s3_client.head_bucket(Bucket=bucket_name)
            return True
        except ClientError as e:
            if "403" not in str(e):
                raise (e)
        return False

    def empty_bucket(self, bucket_name):
        objects = self.s3_client.list_objects(Bucket=bucket_name)

        if "Contents" in objects:
            for object in objects["Contents"]:
                self.s3_client.delete_object(Bucket=bucket_name, Key=object["Key"])

    def get_only_buckets_template_from_cloudformation(self, stack_name):
        template = self.cloudformation_client.get_template(StackName=stack_name)["TemplateBody"]
        template["Resources"] = {k: v for k, v in template["Resources"].items() if v["Type"] == "AWS::S3::Bucket"}
        return template

    def is_stack_exists(self, stack_name):
        stack_exists = False
        try:
            response = self.cloudformation_client.describe_stacks(StackName=stack_name)
            if response["Stacks"][0]["StackStatus"] != "DELETE_COMPLETE":
                stack_exists = True
        except ClientError as e:
            if "does not exist" not in str(e):
                raise (e)
        return stack_exists

    def print_summary(self, filename):
        agg = collections.Counter()
        with open(filename, "r") as fin:
            csv_reader = csv.DictReader(fin)
            for row in csv_reader:
                agg[row.get("inter_az_traffic", "UNKNOWN")] += int(row.get("total_bytes", 0))

        def sizeof_fmt(num, suffix="B"):
            # https://stackoverflow.com/a/1094933
            for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
                if abs(num) < 1024.0:
                    if num > 10:
                        return f"{num:3.0f} {unit}{suffix}"
                    return f"{num:3.1f} {unit}{suffix}"

                num /= 1024.0
            return f"{num:.1f}Yi{suffix}"

        print("SUMMARY:\n------------")
        print(f"TOTAL: {sizeof_fmt(agg.total())}")
        print("TOP APPS:")
        for app, bytes in agg.most_common(10):
            frac = bytes / agg.total()
            hashes = "#" * int(19 * frac)
            print(f"{app[:29] : <30}: [{hashes : <20}] {sizeof_fmt(bytes)} ({frac:.0%})")

    def deploy_cf_stack(self, cf_spec, stack_name, cf_params={}):
        stack_exists = self.is_stack_exists(stack_name)

        if not stack_exists:
            self.log("creating a new cloudformation stack...", is_debug=True)
            self.cloudformation_client.create_stack(
                StackName=stack_name,
                TemplateBody=json.dumps(cf_spec),
                OnFailure="DELETE",
                Parameters=[{"ParameterKey": k, "ParameterValue": v} for k, v in cf_params.items()],
            )
            waiter = self.cloudformation_client.get_waiter("stack_create_complete")
            waiter.wait(StackName=stack_name)
        else:
            self.log("updating an existing cloudformation stack...", is_debug=True)
            try:
                self.cloudformation_client.update_stack(
                    StackName=stack_name,
                    TemplateBody=json.dumps(cf_spec),
                    Parameters=[{"ParameterKey": k, "ParameterValue": v} for k, v in cf_params.items()],
                )
                waiter = self.cloudformation_client.get_waiter("stack_update_complete")
                waiter.wait(StackName=stack_name)
            except ClientError as e:
                if "No updates are to be performed" not in str(e):
                    raise (e)
