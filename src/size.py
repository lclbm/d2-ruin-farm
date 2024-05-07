from loguru import logger
from PIL import ImageGrab

MONITOR_WIDTH, MONITOR_HEIGHT = ImageGrab.grab().size
logger.info(f"屏幕分辨率: {MONITOR_WIDTH}x{MONITOR_HEIGHT}")

if (MONITOR_WIDTH, MONITOR_HEIGHT) not in [(1920, 1080), (2560, 1440)]:
    raise Exception(f"不支持的分辨率，目前仅支持1920x1080和2560x1440分辨率")