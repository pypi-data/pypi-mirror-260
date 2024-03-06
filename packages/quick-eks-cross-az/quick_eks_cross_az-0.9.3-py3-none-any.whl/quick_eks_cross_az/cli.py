"""
The script is based on this work: https://aws.amazon.com/blogs/containers/getting-visibility-into-your-amazon-eks-cross-az-pod-to-pod-network-bytes/
by Kobi Biton, Dor Fibert, and Yazan Khalaf from AWS

Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Modification Notice:
This file has been modified by Asaf Amrami in 2024

"""

import argparse
import sys
from textwrap import dedent

from wakepy import keep

from .lib import CrossAzLogger


def main():
    parser = argparse.ArgumentParser(
        description=dedent(
            """
                Quick EKS Cross AZ Log.
                This script measures cross-AZ (Cross Availability Zone) traffic for EKS (Elastic Kubernetes Service) using flow logs and data from the active Kubernetes context.
                It can be used to estimate associated costs.
                Full docs are here: https://github.com/asafamr/quick-eks-cross-az 
                """
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--minutes", metavar="N", type=int, default=15, help="set the duration for flow logs accumulation in minutes"
    )
    parser.add_argument(
        "--quiet",
        default=False,
        action=argparse.BooleanOptionalAction,
        help="run without manual confirmation",
    )
    parser.add_argument("--verbose", default=False, action=argparse.BooleanOptionalAction, help="verbose log")
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="clean up a previous interrupted run",
    )
    parser.add_argument(
        "--output",
        help="specify output file name",
        default="cross-az.csv",
    )
    parser.add_argument(
        "--stack-name",
        help="override CloudFormation stack name",
        default="quick-eks-cross-az",
    )

    args = parser.parse_args()

    try:
        cazl = CrossAzLogger(
            accumulation_minutes=args.minutes,
            verbose=args.verbose,
            output_file_name=args.output,
            cf_stack_name=args.stack_name,
        )
        cazl.setup_clients()
        credentials_ok = cazl.test_credentials()
        if not credentials_ok:
            return 1
        if args.cleanup:
            print("cleaning up...", flush=True)
            cazl.cleanup_and_delete_cf_stack(args.stack_name)
            return 0
        cluster_name = cazl.get_cluster_name_from_kube_context()
        if not args.quiet:
            print(
                "This script activates flow logs for the cluster's VPC using CloudFormation and then disables them.\n"
                "If the script is interrupted, ensure to clean up resources by running the script with the --cleanup argument.\n"
                "The script is based on this work: https://aws.amazon.com/blogs/containers/getting-visibility-into-your-amazon-eks-cross-az-pod-to-pod-network-bytes/\n"
                "by Kobi Biton, Dor Fibert, and Yazan Khalaf from AWS\n"
                "\n"
                f"Running on active kubernetes context cluster: {cluster_name}\n"
                "Continue? [Y/n]",
                flush=True,
            )
            validation = input()
            if validation.strip().lower() == "n":
                print("aborting...", flush=True)
                return 0
        with keep.running() as _k:
            cazl.run()

    except Exception as e:
        print(f"exception while running script: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
