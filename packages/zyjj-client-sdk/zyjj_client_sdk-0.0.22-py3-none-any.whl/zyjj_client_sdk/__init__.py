import json
import logging

from zyjj_client_sdk.api import Api, TaskStatus
from zyjj_client_sdk.base import Base
from zyjj_client_sdk.storage import Storage
from zyjj_client_sdk.entity import EntityHelper, EntityAudio, EntitySubtitles
from zyjj_client_sdk.ffmpeg_sdk import FFMpegService
from zyjj_client_sdk.client import MqttServer, MqttEventType
from typing import Callable
from tencentcloud.common import credential


# 给回调函数使用的api
class HandleApi:
    def __init__(
            self,
            _base: Base,
            _api: Api,
            uid: str,
            task_id: str,
            _input: dict,
            mqtt: MqttServer,
            global_data: dict
    ):
        self.__base = _base
        self.__api = _api
        self.__ffmpeg = FFMpegService()
        self.__storage = Storage(_base, _api)
        self.__entity = EntityHelper(_base)
        self.__mqtt = mqtt
        self.__global_data = global_data

        self.__uid = uid
        self.__task_id = task_id
        self.__input = _input
        self.__output = {}

    # 更新任务进度
    def progress_update(self, progress: float):
        self.__mqtt.send_task_event(self.__uid, self.__task_id, MqttEventType.Progress, progress)

    # 下载输入的文件并返回耗时信息
    def input_download_and_get_duration_by_key(self, key: str) -> (str, float):
        audio_path = self.__storage.download_file(self.__input[key])
        return audio_path, self.__ffmpeg.get_duration(audio_path) * 1000

    # 获取输入参数cos key的url
    def input_get_tencent_url_by_key(self, key: str) -> str:
        return self.__storage.tencent_get_file_url(self.__input[key]['path'])

    # 获取文件的耗时信息(单位s)
    def input_get_duration_by_key(self, key: str) -> float:
        return self.__input[key]["duration"]

    # 获取任务的原始输入
    def input_get_origin(self) -> dict:
        return self.__input

    # 获取用户积分
    def point_get(self) -> int:
        return self.__api.get_user_point(self.__uid)

    # 检查用户积分
    def point_check(self, point: int):
        if self.__api.get_user_point(self.__uid) < point:
            raise Exception("积分不足请充值")

    # 扣除用户积分
    def point_use(self, name: str, cost: float, desc=''):
        if not self.__api.use_user_point(self.__uid, name, cost, desc):
            raise Exception("积分不足请充值")

    # 上传字幕文件
    def output_upload_subtitle(self, key: str, subtitles: EntitySubtitles):
        subtitle_file = self.__entity.generate_subtitle_file(subtitles)
        self.__output[key] = self.__storage.upload_file(subtitle_file.file_path, self.__uid, 1)

    #  直接上传文件
    def output_upload_file(self, key: str, path: str):
        self.__output[key] = self.__storage.upload_file(path, self.__uid, 1)

    # 设置输出
    def output_set(self, key: str, value: any):
        self.__output[key] = value

    # 获取任务的输出
    def output_get_origin_str(self) -> str:
        return json.dumps(self.__output)

    # 获取任务的输出
    def output_get_origin(self) -> dict:
        return self.__output

    # mqtt发送成功信息
    def success(self, data: dict):
        self.__mqtt.send_task_event(self.__uid, self.__task_id, MqttEventType.Success, data)

    # 从cos下载文件
    def tencent_download_by_key(self, key: str) -> str:
        return self.__storage.tencent_download_file_by_key(key)

    # 从本地上传文件
    def tencent_upload_by_path(self, path: str) -> str:
        return self.__storage.tencent_upload_file_by_path(path, self.__uid)

    # 直接cos key中提取url
    def tencent_get_link_by_key(self, key: str):
        return self.__storage.tencent_get_file_url(key)

    # 获取二进制的url链接
    def tencent_get_link_by_bytes(self, extend: str, data: bytes) -> str:
        # 上传二进制
        key = self.__storage.tencent_upload_bytes(self.__uid, self.__base.generate_filename(extend), data)
        # 获取url
        return self.__storage.tencent_get_file_url(key)

    # 获取腾讯的认证信息
    def tencent_get_credential(self) -> credential.Credential:
        token = self.__api.could_get_tencent_token()
        return credential.Credential(token["TmpSecretId"], token["TmpSecretKey"])

    def config_get_str(self, key: str) -> str:
        return self.__api.get_config(key)

    # 获取配置文件
    def config_get(self, key: str) -> dict:
        return json.loads(self.config_get_str(key))

    #  获取全局数据
    def global_get(self, key: str):
        return self.__global_data[key]


class SdkService:
    def __init__(self):
        self.__base = Base()
        self.__api = Api(self.__base)
        self.__handle = {}
        self.__mqtt = MqttServer(self.__api)
        self.__global_data = {}

    # 添加处理器
    def add_handle(self, task_type: int, handle: Callable[[HandleApi, dict], None]) -> 'SdkService':
        self.__handle[task_type] = handle
        return self

    # 添加全局变量
    def add_global(self, key: str, value: any) -> 'SdkService':
        self.__global_data[key] = value
        return self

    # 启动服务
    def start(self) -> 'SdkService':
        # 后台启动mqtt
        self.__mqtt.start_backend()
        return self

    # 停止服务
    def stop(self) -> 'SdkService':
        self.__mqtt.close()
        return self

    # 开始处理任务
    def execute_task(self) -> dict:
        # 拉取任务
        task_info = self.__api.task_pull_task()
        if task_info is None:
            logging.info("[task] task not found")
            return {"msg": "task not found"}
        logging.info(f'[task] pull task is {task_info}')
        # 获取任务信息
        uid = task_info['uid']
        task_type = task_info['task_type']
        task_input = json.loads(task_info['input'])
        task_id = task_info['id']
        # 寻找处理器
        if task_type in self.__handle:
            self.__mqtt.send_task_event(uid, task_id, MqttEventType.Start, "")
            handle_api = HandleApi(
                self.__base,
                self.__api,
                uid,
                task_id,
                task_input,
                self.__mqtt,
                self.__global_data
            )
            try:
                # 执行任务
                self.__handle[task_type](handle_api, task_input)
                self.__api.task_update_task(
                    task_id,
                    status=TaskStatus.Success,
                    output=handle_api.output_get_origin_str()
                )
                self.__mqtt.send_task_event(
                    uid,
                    task_id,
                    MqttEventType.Success,
                    handle_api.output_get_origin()
                )
                return handle_api.output_get_origin()
            except Exception as e:
                self.__api.task_update_task(task_id, status=TaskStatus.Fail, extra=str(e))
                self.__mqtt.send_task_event(uid, task_id, MqttEventType.Fail, str(e))
                return {"msg": str(e)}
        else:
            err_info = f"task type {task_type} not found"
            logging.error(err_info)
            self.__api.task_update_task(task_id, status=TaskStatus.Fail, extra=err_info)
            self.__mqtt.send_task_event(uid, task_id, MqttEventType.Fail, err_info)
            return {"msg": err_info}
