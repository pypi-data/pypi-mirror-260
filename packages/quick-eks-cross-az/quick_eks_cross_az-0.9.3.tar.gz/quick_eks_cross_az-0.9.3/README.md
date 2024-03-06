# Quick EKS cross az 
This script helps estimating cross az data transfer costs in EKS clusters.

The script is based on an [existing AWS open solution](https://aws.amazon.com/blogs/containers/getting-visibility-into-your-amazon-eks-cross-az-pod-to-pod-network-bytes/).
It simplifies operations by using your current AWS role directly from your shell session, and without using any iam:* permission...


## Features

* **Runs With Your Current AWS Credentials:** Uses the AWS credentials and settings you already have configured in your shell session. No need to configure special credentials just for the demo.
* **Works Without Administrator Privileges:** No need for IAM modification permissions - it's designed to work seamlessly with PowerUser access.  
* **Reuses Your EKS Authentication:** Uses the active Kubernetes context in your shell to retrieve pod and node metadata.
* **Simple Exectuion:** Offers one-line execution with pipx or docker for all orchestration including cleanup.


## Technical Details
Similar to the original solution, this project utilizes CloudFormation to provision flow logs and S3 buckets. However, it orchestrates everything using a script:

* Flow logs are temporarily enabled for the EKS VPC, and necessary S3 buckets are created via CloudFormation.
* Pod metadata, including the `app` label and node IP, is gathered.
* After a configurable timeframe, flow logs are aggregated within Athena.
* The results are downloaded as a CSV file.
* Finally, the script cleans up any infrastructure changes made.


## Getting Started


### Prerequisites
* Python version 3.6 or later
* Kubernetes Cluster API access in current shell
* An active AWS role in your current shell that has permissions to:
    * Create flow logs
    * Create S3 buckets
    * Run Athena queries

#### Using Pipx 

Easiest way to run the script is with [pipx](https://github.com/pypa/pipx). Pipx lets you run Python packages quickly in isolation:

```bash
python3 -m pip install --user pipx # install pipx if required
python3 -m pipx run quick-eks-cross-az --help
```

#### Using Docker
```bash
docker run  -v ~/.kube/config:/kube/config -e KUBECONFIG=/kube/config -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_SESSION_TOKEN  asafamr123/quick-eks-cross-az --help
```



## CLI

```
usage: cli.py [-h] [--minutes N] [--quiet | --no-quiet] [--verbose | --no-verbose]
              [--cleanup | --no-cleanup] [--output OUTPUT] [--stack-name STACK_NAME]

Quick EKS Cross AZ Log
--------
This script measures EKS cross AZ traffic using flow logs and data from active Kubernetes context.
Full docs are here: https://github.com/asafamr/quick-eks-cross-az 

options:
  -h, --help            show this help message and exit
  --minutes N           minutes of flow logs accumulation
  --quiet, --no-quiet   run without manual confirmation
  --verbose, --no-verbose
                        verbose log
  --cleanup, --no-cleanup
                        cleanup a previous interrupted run
  --output OUTPUT       output file name
  --stack-name STACK_NAME
                        override CloudFormation stack name
```