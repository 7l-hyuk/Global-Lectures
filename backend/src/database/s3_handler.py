import boto3
from botocore.exceptions import ClientError

from src.config import AwsSettings, aws_settings


class S3:
    def __init__(self, settings: AwsSettings):
        self.BUCKET_NAME = settings.BUCKET_NAME

        self.client = boto3.client(
            service_name="s3",
            region_name=settings.REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

    def upload_file(
        self,
        file_name: str,
        object_name: str
    ) -> bool:
        try:
            self.client.upload_file(
                file_name,
                self.BUCKET_NAME,
                object_name
            )
        except ClientError as e:
            return False
        return True

    def create_presigned_url(
        self,
        object_name: str,
        expiration: int = 3600
    ) -> str | None:
        try:
            response = self.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.BUCKET_NAME, 'Key': object_name},
                ExpiresIn=expiration,
            )
        except ClientError as e:
            return None
        return response
    
    def get_object(self, object_name: str):
        try:
            s3_object = self.client.get_object(Bucket=self.BUCKET_NAME, Key=object_name)
        except ClientError as e:
            return None
        return s3_object["Body"].read()


s3 = S3(aws_settings)
