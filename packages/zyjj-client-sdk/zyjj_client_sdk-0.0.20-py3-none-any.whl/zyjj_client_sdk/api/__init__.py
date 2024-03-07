import json
import logging

import requests
from zyjj_client_sdk.base import Base
from zyjj_client_sdk.api.model import TaskStatus


class Api:
    def __init__(self, base: Base):
        self.__header = {
            "x-username": base.username,
            "x-password": base.password,
            "Content-Type": "application/json"
        }
        self.__base = f"{base.host}/api/v1/client"

    def __request(self, method: str, path: str, data: dict = None):
        url = f"{self.__base}/{path}"
        logging.info(f"request url {url}")
        res = None
        if method == "get":
            res = requests.get(url, headers=self.__header)
        elif method == "put":
            res = requests.put(url, data=json.dumps(data), headers=self.__header)
        elif method == "post":
            res = requests.post(url, data=json.dumps(data), headers=self.__header)
        elif method == "delete":
            res = requests.delete(url, headers=self.__header)
        if res is None:
            logging.info("[request] request res is none")
        elif res.status_code != 200:
            logging.info(f"[request] request status code is {res.status_code}, res is {res.text}")
            raise Exception("server error")
        else:
            res = res.json()
            if "code" in res and res["code"] != 0:
                raise Exception(res["msg"])
            else:
                return res["data"]
        return {}

    # 获取腾讯云token
    def could_get_tencent_token(self):
        return self.__request("get", "cloud/tencent/token")

    # 获取腾讯云cos秘钥信息
    def could_get_tencent_cos(self):
        return self.__request("get", "cloud/tencent/cos")

    # 获取火山语音信息
    def cloud_get_volcano_voice(self):
        return self.__request("get", "cloud/volcano/voice")

    # 获取MQTT
    def cloud_get_mqtt(self):
        return self.__request("get", f"cloud/mqtt/task")

    # 拉取任务
    def task_pull_task(self):
        return self.__request("get", "task/pull")

    # 更新任务状态
    def task_update_task(
            self,
            task_id: str,
            status: TaskStatus = None,
            point_cost: float = None,
            output: str = None,
            extra: str = None
    ):
        data = {}
        if status is not None:
            data["status"] = status.value
        if output is not None:
            data["output"] = output
        if extra is not None:
            data["extra"] = extra
        if point_cost is not None:
            data["point_cost"] = point_cost
        return self.__request("put", f"task/{task_id}", data)

    # 获取用户积分
    def get_user_point(self, uid: str) -> int:
        return self.__request("get", f"point/user/{uid}", {})

    # 扣除用户积分
    def use_user_point(self, uid: str, name: str, point: float, desc='') -> bool:
        logging.info("[api] {} use point {}".format(uid, int(point)))
        try:
            self.__request("post", "point/deducting", {
                "uid": uid,
                "name": name,
                "point": int(point),
                "desc": desc,
            })
            return True
        except Exception as e:
            print("use_user_point error", e)
            return False

    # 获取配置
    def get_config(self, key: str) -> str:
        return self.__request("get", f"config/{key}")["value"]
