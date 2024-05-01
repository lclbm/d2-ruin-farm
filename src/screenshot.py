import cv2
import numpy as np
from PIL import ImageGrab, Image

from size import (
    MONITOR_WIDTH,
    X_BBOX,
    HP_BAR_BBOX,
    BOSS_HP_BAR_BBOX,
)


def log_image(func: callable):
    from loguru import logger
    from functools import wraps
    from datetime import datetime
    from settings import base_settings

    @wraps(func)
    def inner():
        image = func()
        if base_settings.debug:
            time_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
            file_name = f"{func.__name__}_{time_str}.png"
            
            logger.debug(f"保存图片: {file_name}")
            image.save(f"./debug/{file_name}")
        return image

    return inner


@log_image
def get_x_image():
    return ImageGrab.grab(bbox=X_BBOX)


@log_image
def get_hp_bar_image():
    return ImageGrab.grab(bbox=HP_BAR_BBOX)


@log_image
def get_boss_hp_bar_image():
    return ImageGrab.grab(bbox=BOSS_HP_BAR_BBOX)


def conver_image_to_open_cv(image: Image.Image):
    import cv2
    import numpy as np

    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)


def get_template_similarity(image: Image.Image, template: cv2.typing.MatLike):
    image_cv = conver_image_to_open_cv(image)
    result = cv2.matchTemplate(image_cv, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    return min_val


def get_mask_ratio(image: np.ndarray, lower_bound: np.ndarray, upper_bound: np.ndarray):
    mask = cv2.inRange(image, lower_bound, upper_bound)
    return np.sum(mask == 255) / (image.size / 3)


NORMAL_HP_COLOR_RANGE = (
    np.array([200, 200, 200][::-1]),
    np.array([255, 255, 255][::-1]),
)
FINISH_HP_COLOR_RANGE = (np.array([0, 190, 190][::-1]), np.array([0, 200, 200][::-1]))
BOSS_HP_COLOR_RANGE = (np.array([150, 90, 10][::-1]), np.array([240, 180, 80][::-1]))
X_TEMPLATE_IMAGE_CV = conver_image_to_open_cv(
    Image.open(f"./asset/x_{MONITOR_WIDTH}.png")
)


def get_x_similarity():
    return get_template_similarity(get_x_image(), X_TEMPLATE_IMAGE_CV)


def get_finish_hp_bar_mask_ratio():
    return get_mask_ratio(
        conver_image_to_open_cv(get_hp_bar_image()), *FINISH_HP_COLOR_RANGE
    )


def get_normal_hp_bar_mask_ratio():
    return get_mask_ratio(
        conver_image_to_open_cv(get_hp_bar_image()), *NORMAL_HP_COLOR_RANGE
    )


def get_boss_hp_bar_mask_ratio():
    return get_mask_ratio(
        conver_image_to_open_cv(get_boss_hp_bar_image()), *BOSS_HP_COLOR_RANGE
    )
