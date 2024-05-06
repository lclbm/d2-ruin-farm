from loguru import logger
from PIL import ImageGrab

MONITOR_WIDTH, MONITOR_HEIGHT = ImageGrab.grab().size
logger.info(f"屏幕分辨率: {MONITOR_WIDTH}x{MONITOR_HEIGHT}")

if (MONITOR_WIDTH, MONITOR_HEIGHT) not in [(1920, 1080), (2560, 1440)]:
    raise Exception(f"不支持的分辨率，目前仅支持1920x1080和2560x1440分辨率")

RESIZE_RATIO = MONITOR_WIDTH / 2560
resize = lambda x: int(x * RESIZE_RATIO)


def get_resize(*x: int):
    if len(x) == 1:
        return resize(x[0])

    return tuple(map(resize, x))


X_START_POSITION = get_resize(252, 1233)
X_WIDTH, X_HEIGHT = get_resize(82, 85)

HP_BAR_POSITION = get_resize(994, 134)
HP_BAR_WIDTH, HP_BAR_HEIGHT = get_resize(100, 10)

BOSS_HP_BAR_POSITION = get_resize(1250, 1295)
BOSS_HP_BAR_WIDTH, BOSS_HP_BAR_HEIGHT = get_resize(100, 10)

X_BBOX = (
    *X_START_POSITION,
    X_START_POSITION[0] + X_WIDTH,
    X_START_POSITION[1] + X_HEIGHT,
)
HP_BAR_BBOX = (
    *HP_BAR_POSITION,
    HP_BAR_POSITION[0] + HP_BAR_WIDTH,
    HP_BAR_POSITION[1] + HP_BAR_HEIGHT,
)
BOSS_HP_BAR_BBOX = (
    *BOSS_HP_BAR_POSITION,
    BOSS_HP_BAR_POSITION[0] + BOSS_HP_BAR_WIDTH,
    BOSS_HP_BAR_POSITION[1] + BOSS_HP_BAR_HEIGHT,
)
