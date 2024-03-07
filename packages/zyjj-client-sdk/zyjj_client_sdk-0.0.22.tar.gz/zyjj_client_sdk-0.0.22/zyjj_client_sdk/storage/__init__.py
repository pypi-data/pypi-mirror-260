import json
import logging

from zyjj_client_sdk.api import Api
from zyjj_client_sdk.base import Base
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from typing import Callable


def _callback(i: float):
    logging.info(f"[storage] current progress {i}")


class Storage:
    def __init__(self, base: Base, api: Api):
        self.__base = base
        self.__api = api
        self.__auth = None

    def __get_auth(self):
        if self.__auth is None:
            self.__auth = self.__api.could_get_tencent_cos()
        return self.__auth

    # 下载文件
    def download_file(self, data: dict) -> str:
        key = data['path']
        path = self.__base.generate_file_with_path(key)
        self.__tencent_download_file(key, path, _callback)
        return path

    # 上传文件
    def upload_file(self, path: str, uid: str, source: int) -> dict:
        key = self.__tencent_upload_file(path, uid, _callback)
        return {
            "name": path.split("/")[-1],
            "path": key,
            "source": source
        }

    # 原始下载文件
    def tencent_download_file_by_key(self, key: str) -> str:
        path = self.__base.generate_file_with_path(key)
        self.__tencent_download_file(key, path, _callback)
        return path

    # 直接上传文件
    def tencent_upload_file_by_path(self, path: str, uid: str) -> str:
        return self.__tencent_upload_file(path, uid, _callback)

    def __tencent_get_client(self) -> CosS3Client:
        auth = self.__get_auth()
        token = auth["token"]
        config = CosConfig(
            Region=auth["region"],
            SecretId=token["TmpSecretId"],
            SecretKey=token["TmpSecretKey"],
            Token=token["Token"],
            Scheme="https",
        )
        return CosS3Client(config)

    # 下载腾讯存储文件
    def __tencent_download_file(self, key: str, path: str, callback: Callable[[float], None] = None):
        client = self.__tencent_get_client()
        client.download_file(
            Bucket=self.__auth["bucket"],
            Key=key,
            DestFilePath=path,
            progress_callback=callback,
        )

    def __tencent_upload_file(self, path: str, uid: str, callback: Callable[[float], None] = None) -> str:
        client = self.__tencent_get_client()
        key = f"tmp/{uid}/{self.__base.generate_file_with_path(path).split('/')[-1]}"
        client.upload_file(
            Bucket=self.__auth["bucket"],
            Key=key,
            LocalFilePath=path,
            progress_callback=callback,
        )
        return key

    # 上传二进制数据
    def tencent_upload_bytes(self, uid: str, key: str, data: bytes) -> str:
        client = self.__tencent_get_client()
        key = f"tmp/{uid}/{key}"

        class TmpBody:
            def __init__(self, _data: bytes):
                self.__data = _data

            def read(self, n: int) -> bytes:
                if n >= len(self.__data):
                    _data = self.__data
                    self.__data = bytes()
                    return _data
                else:
                    _data = self.__data[:n]
                    self.__data = self.__data[n - 1:]
                    return _data

        client.upload_file_from_buffer(
            Bucket=self.__auth["bucket"],
            Key=key,
            Body=TmpBody(data),
        )
        return key

    def tencent_get_file_url(self, key: str, expired=180) -> str:
        client = self.__tencent_get_client()
        return client.get_presigned_download_url(
            Bucket=self.__auth["bucket"],
            Key=key,
            Expired=expired,
            Params={
                "x-cos-security-token":
                    self.__auth["token"]["Token"]
            }
        )
