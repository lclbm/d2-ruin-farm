import cv2
import numpy as np
from PIL import Image, ImageGrab

MONITOR_WIDTH, MONITOR_HEIGHT = ImageGrab.grab().size

if MONITOR_WIDTH == 1920 and MONITOR_HEIGHT == 1080:
    ...


elif MONITOR_WIDTH == 2560 and MONITOR_HEIGHT == 1440:
    X_START_POSITION = (252, 1233)
    X_WIDTH, X_HEIGHT = (82, 85)

    HP_BAR_POSITION = (994, 134)
    HP_BAR_WIDTH, HP_BAR_HEIGHT = (100, 10)

    BOSS_HP_BAR_POSITION = (1250, 1295)
    BOSS_HP_BAR_WIDTH, BOSS_HP_BAR_HEIGHT = (100, 10)
else:
    raise Exception("Unsupported monitor resolution")


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


def get_x_image():
    return ImageGrab.grab(bbox=X_BBOX)


def get_hp_bar_image():
    return ImageGrab.grab(bbox=HP_BAR_BBOX)


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
    Image.open(f"../asset/x_{MONITOR_WIDTH}.png")
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
