import tomllib
import dataclasses
from pathlib import Path

from size import MONITOR_HEIGHT

SETTINGS_PATH = Path(f"./settings.toml")


@dataclasses.dataclass
class BaseSettings:
    log_level: str
    debug: bool
    kick_mode: int
    map_debug: bool


@dataclasses.dataclass
class KeySettings:
    职业技能按键: str
    未充能近战按键: str
    跳隐身按键: str
    终结技按键: str
    埋头表情按键: str


@dataclasses.dataclass
class ImageSettings:
    @dataclasses.dataclass
    class MonitorSettings:
        X技能坐标边界: list[int]
        玩家血条坐标边界: list[int]
        BOSS血条坐标边界: list[int]

    x技能识别阈值: float

    连续检测boss血条次数: int
    连续检测玩家血条次数: int

    玩家血条颜色范围: list[list[int]]
    玩家终结技血条颜色范围: list[list[int]]
    BOSS血条颜色范围: list[list[int]]

    monitor_settings: MonitorSettings


@dataclasses.dataclass
class MapSelecteSettings:
    @dataclasses.dataclass
    class MonitorSettings:
        鼠标x轴坐标: list[int]
        难度选项卡坐标: list[int]
        大师难度选项坐标: list[int]
        开始按钮坐标: list[int]
        F进度坐标: list[int]

    鼠标移动和单击时间间隔: float
    打开地图后等待时间: float
    选择废墟等待时间: float
    选择难度时间间隔: float
    飞图点击开始按钮延迟: float

    monitor_settings: MonitorSettings


@dataclasses.dataclass
class KickSettings:
    @dataclasses.dataclass
    class Command:
        开BOSS鼠标偏移: tuple[int]
        隐身后往左走时间: float
        隐身后往前走时间: float

        射击黄血鼠标偏移: tuple[int]
        等待黄血刷新时间: float

        躲藏第一段位移镜头偏移: tuple[int]
        躲藏第一段位移时间: float

        躲藏第二段位移镜头偏移: tuple[int]
        躲藏第二段位移时间: float

    最大连续失败次数: int
    闪身后破隐等待时间: float
    终结后最长等待结算时间: float
    未检测到护盾后的等待时间: float
    等待结算超时后的等待时间: float

    command: Command


settings = tomllib.loads(SETTINGS_PATH.read_text("utf-8"))
image_monitor_settings = {h: settings["image"].pop(f"{h}p") for h in [1080, 1440]}
map_select_monitor_settings = {
    h: settings["map_select"].pop(f"{h}p") for h in [1080, 1440]
}
commands = settings["kick"].pop("commands")

base_settings = BaseSettings(**settings.pop("base"))
key_settings = KeySettings(**settings.pop("key"))
image_settings = ImageSettings(
    **settings.pop("image"),
    monitor_settings=ImageSettings.MonitorSettings(
        **image_monitor_settings[MONITOR_HEIGHT]
    ),
)
map_selecte_settings = MapSelecteSettings(
    **settings.pop("map_select"),
    monitor_settings=MapSelecteSettings.MonitorSettings(
        **(map_select_monitor_settings[MONITOR_HEIGHT])
    ),
)
kick_settings = KickSettings(
    **settings.pop("kick"),
    command=KickSettings.Command(**commands[base_settings.kick_mode]),
)
