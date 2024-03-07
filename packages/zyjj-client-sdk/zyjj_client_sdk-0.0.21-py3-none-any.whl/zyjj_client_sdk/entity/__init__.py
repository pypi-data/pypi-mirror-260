import datetime
from zyjj_client_sdk.base import Base
from zyjj_client_sdk.entity.model import EntitySubtitles, EntitySubtitleFile, EntityAudio, EntityText, EntityTexts, EntitySubtitle


def convert_milliseconds_to_time(milliseconds):
    # 将毫秒时间戳转换为timedelta对象
    delta = datetime.timedelta(milliseconds=milliseconds)
    # 将timedelta对象转换为datetime对象
    dt = datetime.datetime(1, 1, 1) + delta
    # 将datetime对象格式化为字符串，格式为"HH:MM:SS,mmm"
    time_str = dt.strftime("%H:%M:%S,%f")[:-3]

    return time_str


class EntityHelper:
    def __init__(self, base: Base):
        self.__base = base

    # 字幕生成
    def generate_subtitle_file(self, subtitles: EntitySubtitles) -> EntitySubtitleFile:
        file_path = self.__base.generate_local_file("srt")
        with open(file_path, "w") as f:
            for index in range(len(subtitles.subtitles)):
                subtitle = subtitles.subtitles[index]
                f.write(f"{index}\n")
                f.write(f"{convert_milliseconds_to_time(subtitle.time_start)} "
                        f"--> {convert_milliseconds_to_time(subtitle.time_end)}\n")
                f.write(f"{subtitle.content}\n\n")
        return EntitySubtitleFile(file_path, subtitles.duration)

    @staticmethod
    def generate_texts(text_list: list[str]) -> EntityTexts:
        texts = []
        for text in text_list:
            texts.append(EntityText(text))
        return EntityTexts(texts)

    # 生成音频文件
    def generate_audio(self, data: bytes, duration: int = 0) -> EntityAudio:
        path = self.__base.generate_local_file("wav")
        open(path, "wb").write(data)
        return EntityAudio(path, duration)
