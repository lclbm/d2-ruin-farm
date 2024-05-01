import re
import tomllib
import dataclasses
from pathlib import Path
from loguru import logger

from size import MONITOR_HEIGHT

SETTINGS_PATH = Path(f"./settings.toml")


@dataclasses.dataclass
class BaseSettings:
    debug: bool
    职业技能按键: str
    未充能近战按键: str
    跳隐身按键: str
    终结技按键: str
    埋头表情按键: str


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


settings = tomllib.loads(SETTINGS_PATH.read_text("utf-8"))
base_settings = BaseSettings(**settings.pop("base"))
monitor_settings = Config(**settings.pop(f"{MONITOR_HEIGHT}p"))

logger.info(base_settings)
logger.info(monitor_settings)
