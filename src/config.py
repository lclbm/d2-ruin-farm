import tomllib
import dataclasses
from pathlib import Path
from loguru import logger

from size import MONITOR_WIDTH


@dataclasses.dataclass
class Config:
    开boss鼠标偏移: tuple[int]
    隐身后往左走时间: float
    隐身后往前走时间: float

    射击黄血鼠标偏移: tuple[int]
    等待黄血刷新时间: float

    躲藏第一段位移镜头偏移: tuple[int]
    躲藏第一段位移时间: float

    躲藏第二段位移镜头偏移: tuple[int]
    躲藏第二段位移时间: float


config = Config(
    **tomllib.loads(Path(f"./config_{MONITOR_WIDTH}.toml").read_text("utf-8"))
)
logger.info(config)