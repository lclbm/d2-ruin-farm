import time
import pydirectinput
from pydirectinput import (
    keyDown,
    keyUp,
    leftClick,
    move,
    moveTo,
    mouseUp,
    mouseDown,
    RIGHT,
    press,
)
from loguru import logger


pydirectinput.PAUSE = 0


def press_and_hold_key(key: str, seconds: float):
    logger.debug(f'press key "{key}" {seconds} seconds')

    keyDown(key)
    time.sleep(seconds)
    keyUp(key)


def move_to_and_left_click(x: int = None, y: int = None):
    logger.debug(f"move to ({x}, {y}) and left click")

    pydirectinput.moveTo(x, y)
    time.sleep(0.2)
    pydirectinput.leftClick()


def run(secons: float):
    keyDown("shiftleft")
    time.sleep(0.001)
    keyDown("w")
    time.sleep(secons)
    keyUp("shiftleft")
    keyUp("w")


def open_map_and_switch_difficulty():
    # 打开地图
    press("m")
    time.sleep(1)

    # 点击战争领主的废墟
    moveTo(2360)
    time.sleep(0.3)
    leftClick()

    # 点开难度选择
    time.sleep(1.5)
    move_to_and_left_click(1960, 1110)

    # 选择大师难度
    time.sleep(1.5)
    move_to_and_left_click(455, 460)


def start_next_round():
    open_map_and_switch_difficulty()

    # 点击开始
    time.sleep(2)
    move_to_and_left_click(2180, 1210)


def refresh_checkpoint():
    open_map_and_switch_difficulty()

    # F进度
    moveTo(1805, 1115)
    time.sleep(1)
    press_and_hold_key("f", 4)

    for _ in range(2):
        press("esc")
        time.sleep(0.5)

    run(10)
    logger.info("已重置进度")


def kick_boss_by_indebted_kindess():
    # 切枪
    press("2")
    time.sleep(2)

    # 开启boss
    move(-40, -55, relative=True)
    time.sleep(0.5)
    leftClick()
    time.sleep(0.2)

    # 跳x隐身
    press("space")
    time.sleep(0.2)
    press("x")
    time.sleep(1)

    # 移动到预设的位置
    press_and_hold_key("a", 0.5)
    press_and_hold_key("w", 1.83)

    # 射击黄血小怪
    mouseDown(button=RIGHT)
    time.sleep(0.3)
    move(184, 95, relative=True)
    time.sleep(5.805)
    leftClick()
    mouseUp(button=RIGHT)

    # 终结小怪
    keyDown("g")
    run(1.7)
    keyUp("g")


def hide_indebted_kindess():
    move(-820, 0, relative=True)
    keyDown("w")
    keyDown("shiftleft")
    time.sleep(1.6)
    move(200, 0, relative=True)
    time.sleep(2.4)

    keyUp("shiftleft")
    keyUp("w")
    time.sleep(0.5)
    press("down")
