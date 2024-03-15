from functools import lru_cache
from typing import Protocol

from aioboto3 import Session
from botocore.client import BaseClient
from botocore.config import Config
from fastapi import UploadFile

from app.core.config import get_settings
from app.storage.exception_handler import Boto3ErrorHandler

EXPIRATION_TIME = 60 * 60


class FileManager(Protocol):
    @Boto3ErrorHandler()
    async def create_presigned_url(self, file_name: str, expiration_time: int = EXPIRATION_TIME) -> str | None: ...

    @Boto3ErrorHandler(return_value=False)
    async def upload_file(self, file: UploadFile, file_name: str) -> bool: ...

    @Boto3ErrorHandler(return_value=False)
    async def delete_objects(self, file_name: str) -> bool: ...


class S3Manager(FileManager):
    def __init__(self, bucket: str, endpoint_url: str):
        self.bucket = bucket
        self.endpoint_url = endpoint_url

    @property
    def __session_s3_client(self) -> BaseClient:
        session = Session()
        session_client = session.client(
            service_name='s3',
            config=Config(signature_version='s3v4'),
            endpoint_url=self.endpoint_url,
        )
        return session_client

    @Boto3ErrorHandler()
    async def create_presigned_url(self, file_name: str, expiration_time: int = EXPIRATION_TIME) -> str | None:
        async with self.__session_s3_client as s3:
            presigned_url = await s3.generate_presigned_url(
                ClientMethod='get_object',
                Params={'Bucket': self.bucket, 'Key': file_name},
                ExpiresIn=expiration_time,
            )
        return presigned_url

    @Boto3ErrorHandler(return_value=False)
    async def upload_file(self, file: UploadFile, file_name: str) -> bool:
        async with self.__session_s3_client as s3:
            await s3.upload_fileobj(file, Key=file_name, Bucket=self.bucket)
        return True

    @Boto3ErrorHandler(return_value=False)
    async def delete_objects(self, file_name: str) -> bool:
        async with self.__session_s3_client as s3:
            await s3.delete_object(Bucket=self.bucket, Key=file_name)
        return True


@lru_cache
def get_s3() -> S3Manager:
    return S3Manager(
        bucket=get_settings().AWS_S3_CARS_BUCKET_NAME,
        endpoint_url=get_settings().AWS_S3_ENDPOINT_URL,
    )
