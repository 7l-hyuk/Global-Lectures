import boto3
from botocore.exceptions import ClientError
from src.config import aws_settings, AwsSettings
from src.utils.logger import logger


class S3:
    def __init__(self, settings: AwsSettings):
        self.BUCKET_NAME = settings.BUCKET_NAME
        self.client = boto3.client(
            service_name="s3",
            region_name=settings.REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

    def upload_file(self, file_name: str, object_name: str):
        try:
            self.client.upload_file(
                file_name,
                self.BUCKET_NAME,
                object_name
            )
        except ClientError as e:
            logger.error(e)
            return False
        return True

s3 = S3(aws_settings)
print(s3.client)