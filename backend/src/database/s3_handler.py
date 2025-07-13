import threading
import boto3
from botocore.exceptions import ClientError

from src.config import AwsSettings, aws_settings
from src.path_manager import UserPathContext, UserFile


class S3UploadFileConfig:
    def __init__(
        self,
        video_id: int,
        target_lang: str,
        source_lang: str | None = None
    ):
        audio_key_format = lambda video_id, lang: f"audios/{video_id}/{lang}.wav"
        subtitle_key_format = lambda video_id, lang: f"subtitles/{video_id}/{lang}.json"

        self.target_audio_key = audio_key_format(video_id, target_lang)
        self.target_subtitle_key = subtitle_key_format(video_id, target_lang)

        if source_lang:
            self.video_key = f"videos/{video_id}.mp4"
            self.source_audio_key = audio_key_format(video_id, source_lang)
            self.source_subtitle_key = subtitle_key_format(video_id, source_lang)

    def mapping_file(self, user_path_ctx: UserPathContext):
        keys = [self.target_audio_key, self.target_subtitle_key]
        files = [
            user_path_ctx.get_path(UserFile.AUDIO.DUBBING),
            user_path_ctx.get_path(UserFile.SUBTITLE.TARGET)
        ]
        if hasattr(self, "video_key"):
            keys += [self.video_key, self.source_audio_key, self.source_subtitle_key]
            files += [
                user_path_ctx.get_path(UserFile.VIDEO.NO_VOCAL),
                user_path_ctx.get_path(UserFile.AUDIO.VOCALS),
                user_path_ctx.get_path(UserFile.SUBTITLE.SOURCE)
            ]
        files = list(map(str, files))

        return [
            {"object_name": key, "file_name": file}
            for key, file in zip(keys, files)
        ]


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

    def upload_files(
        self,
        upload_config: S3UploadFileConfig,
        user_path_ctx: UserPathContext
    ):
        threads: list[threading.Thread] = []
        for config in upload_config.mapping_file(user_path_ctx):
            t = threading.Thread(target=self.upload_file, kwargs=config)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

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
