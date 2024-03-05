# 字幕数据
from dataclasses import dataclass


# 文本数据
@dataclass
class EntityText:
    text: str  # 文本内容


# 文本列表
@dataclass
class EntityTexts:
    texts: list[EntityText]  # 文本列表


# 音频数据
@dataclass
class EntityAudio:
    file_path: str
    duration: float = 0  # 持续时间(毫秒)


@dataclass
class EntitySubtitle:
    time_start: int  # 开始时间,毫秒
    time_end: int  # 结束时间，毫秒
    content: str  # 字幕内容


# 字幕数据集合
@dataclass
class EntitySubtitles:
    subtitles: list[EntitySubtitle]  # 字幕列表
    duration: int = 0  # 持续时间 ms
    lang: int = 1  # 语言 1 中文 2 英语


# 字幕数据
@dataclass
class EntitySubtitleFile:
    file_path: str  # 文件路径
    duration: int = 0  # 持续时间
    subtitles_list: list[EntitySubtitles] = None  # 字幕列表
