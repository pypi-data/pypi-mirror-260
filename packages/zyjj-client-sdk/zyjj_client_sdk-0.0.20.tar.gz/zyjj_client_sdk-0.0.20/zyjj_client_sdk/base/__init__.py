import json
import logging
import uuid


class Base:
    def __init__(self):
        with open("config.json", "r") as f:
            data = json.loads(f.read())
            logging.info(f"config info {data}")
            self.username = data["username"]
            self.password = data["password"]
            self.host = data["host"]
            self.__config = data
            self.tmp_dir = "/tmp"

    # 生成一个临时文件
    def generate_file(self, extend: str) -> str:
        return f"{self.tmp_dir}/{str(uuid.uuid4())}.{extend}"

    # 根据路径生成一个新的同名文件
    def generate_file_with_path(self, path: str) -> str:
        return self.generate_file(path.split(".")[-1])

    # 获取配置文件
    def get_config_data(self, key: str):
        return self.__config[key]
