"""
AWS_CF Class
Class containing all the needed AWS Service Manager actions and the client itself.
"""
import os
from typing import Optional
import json
import boto3

from data_analytics_core.localstack.boto_client_moks.localstack_clients import boto3_client_localstack


class AmazonWebServicesCF:
    def __init__(self, region_name="eu-central-1"):
        # env aws connections generation
        self.region_name = region_name
        if os.getenv("LOCALSTACK_ENDPOINT_URL"):
            self.cf_client = boto3_client_localstack(service_name="cloudformation", region_name=region_name)
        else:
            self.cf_client = boto3.client('cloudformation', region_name=region_name)

    def create_resource(self, resource_name: str, path_to_file: str, role_arn: str = None, tags: list[dict] = None):
        self.cf_client.create_stack(
            StackName=resource_name,
            TemplateURL=path_to_file,
            RoleARN=role_arn,
            OnFailure="ROLLBACK",
            Tags=tags
        )
