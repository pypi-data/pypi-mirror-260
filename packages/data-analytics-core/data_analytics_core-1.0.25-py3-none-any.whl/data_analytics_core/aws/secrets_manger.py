"""
AWS_SM Class
Class containing all the needed AWS Secrets Manager actions and the client itself.
"""
import os
from typing import Optional
import boto3
# custom imports
from data_analytics_core.localstack.boto_client_moks.localstack_clients import boto3_client_localstack


class AmazonWebServicesSecretsManager:
    def __init__(self, region_name="eu-central-1"):
        # env aws connections generation
        self.region_name = region_name
        if os.getenv("LOCALSTACK_ENDPOINT_URL"):
            self.sm_client = boto3_client_localstack(service_name="secretsmanager", region_name=region_name)
        else:
            self.sm_client = boto3.client('secretsmanager', region_name=region_name)

    def extract_secret_value_as_str(self, secret_arn_or_name: str) -> Optional[str]:
        return self.sm_client.get_secret_value(SecretId=secret_arn_or_name)["SecretString"]

    def create_secret(self, name: str, secret_value: str, description=Optional[str],
                      kms_key=Optional[str], tags=Optional[list]):
        """
        :param name:
        :param secret_value:
        :param description:
        :param kms_key: This parameter can be the ARN, ID or even the alias given to such key.
        :param tags:
        :return:
        """
        self.sm_client.create_secret(
            Name=name,
            Description=description,
            KmsKeyId=kms_key,
            SecretString=secret_value,
            Tags=tags
        )

    def get_secret_arn(self, secret_name: str):
        return self.sm_client.get_secret_value(SecretId=secret_name)["SecretString"]
