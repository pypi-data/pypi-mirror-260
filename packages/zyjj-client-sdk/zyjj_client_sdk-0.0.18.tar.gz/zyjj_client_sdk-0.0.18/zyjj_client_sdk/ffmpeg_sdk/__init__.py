import logging
import os
import ffmpeg
from ffmpeg_progress_yield import FfmpegProgress
from typing import Callable


def show_progress():
    def handle(process: int, frame: int, fps: int, speed: str):
        logging.info(f" progress {process}, frame {frame}, fps {fps}, speed {speed}")

    return handle


def get_abs_path(file_path: str) -> str:
    return os.path.abspath(file_path)


def get_abs_path_list(file_path_list: list[str]) -> list[str]:
    return list(map(get_abs_path, file_path_list))


class FFMpegService:
    def __init__(self):
        self.__thread = 4
        self.__hwaccels = 'cuda'  # cuda dxva2 qsv d3d11va
        pass

    # ffmpeg命令处理
    def ffmpeg_progress(self, f, target: str, callback: Callable[[float], None]):
        cmd = f.output(target, threads=self.__thread).compile()
        print(cmd)
        ff = FfmpegProgress(cmd)
        for progress in ff.run_command_with_progress():
            callback(progress)

    # 合并多条wav文件
    def merge_wav(self, source_list: list[str], target: str, callback: Callable[[float], None]):
        file_list = [ffmpeg.input(source) for source in source_list]
        self.ffmpeg_progress(ffmpeg.concat(*file_list, a=1, v=0), target, callback)

        cmd = ffmpeg.concat(*file_list, a=1, v=0).output(target, threads=self.__thread).compile()
        ff = FfmpegProgress(cmd)
        for progress in ff.run_command_with_progress():
            print(f"{progress}/100")

    # 添加字幕文件
    def video_subtitle(self, video: str, subtitle: str, target: str, callback: Callable[[float], None]):
        self.ffmpeg_progress(ffmpeg.input(video).filter("subtitles", subtitle), target, callback)

    @staticmethod
    # 获取文件时长(s)
    def get_duration(path: str) -> float:
        probe = ffmpeg.probe(path)
        print(probe)
        return float(probe["format"]["duration"])
