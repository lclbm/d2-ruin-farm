import time
from pathlib import Path
from loguru import logger

X_SIMILARITY_CHECK_INTERVAL = 4
BOSS_HP_BAR_CHECK_INTERVAL = 0.5


def run():
    from pydirectinput import press
    from screenshot import (
        get_x_similarity,
        get_finish_hp_bar_mask_ratio,
        check_boss_hp_bar,
        check_normal_hp_bar,
    )
    from directx import (
        kick_boss_by_indebted_kindess,
        start_next_round,
        refresh_checkpoint,
        hide_indebted_kindess,
    )
    from settings import (
        base_settings,
        key_settings,
        image_settings,
        map_selecte_settings,
        kick_settings,
    )

    logger.add("./logs/d2-ruin-farm_{time}.log", level=base_settings.log_level)
    for settings in [
        base_settings,
        key_settings,
        image_settings,
        map_selecte_settings,
        kick_settings,
    ]:
        logger.info(settings)

    start_count = 0
    finish_count = 0
    success_count = 0
    continuous_fail_count = 0
    need_refresh_checkpoint = False

    logger.info("程序启动")

    if base_settings.debug:
        logger.info("已开启调试模式")
        Path("./debug").mkdir(exist_ok=True)

    time.sleep(2)

    if base_settings.map_debug:
        logger.info("已开始进行地图调试，请检查自动飞本逻辑是否正常")
        start_next_round()
        need_refresh_checkpoint = True

    while True:
        while True:
            x_similarity = get_x_similarity()
            if x_similarity > image_settings.x技能识别阈值:
                logger.info("检测到X技能准备就绪")
                break
            time.sleep(X_SIMILARITY_CHECK_INTERVAL)

        if continuous_fail_count >= kick_settings.最大连续失败次数:
            logger.info(f"连续失败次数超过{kick_settings.最大连续失败次数}次，重新进本")
            start_next_round()
            need_refresh_checkpoint = True
            continuous_fail_count = 0
            continue

        if need_refresh_checkpoint:
            refresh_checkpoint()
            need_refresh_checkpoint = False
            continue

        logger.info(
            f"start_count: {start_count}, finish_count: {finish_count}, success_count: {success_count}"
        )
        start_count += 1

        kick_boss_by_indebted_kindess()
        time.sleep(0.1)

        finish_hp_bar_mask_ratio = get_finish_hp_bar_mask_ratio()

        if not finish_hp_bar_mask_ratio >= 0.8:
            continuous_fail_count += 1
            logger.info("未在玩家血条上检测到感应护盾，准备团灭重试")

            press(key_settings.职业技能按键)
            time.sleep(kick_settings.闪身后破隐等待时间)
            press(key_settings.未充能近战按键)
            time.sleep(kick_settings.未检测到护盾后的等待时间)

            continue

        finish_count += 1
        logger.info("玩家血条蓝盾检测成功")

        start_time = time.monotonic()

        # 躲起来等待boss血条消失
        time.sleep(2)
        hide_indebted_kindess()

        while True:
            if time.monotonic() - start_time >= kick_settings.终结后最长等待结算时间:
                continuous_fail_count += 1
                logger.info("等待boss血条消失超时，准备团灭重试")

                press(key_settings.未充能近战按键)
                time.sleep(kick_settings.等待结算超时后的等待时间)

                break

            # 如果boss血条消失，进行玩家血条的检测
            if check_boss_hp_bar(
                image_settings.连续检测boss血条次数,
                BOSS_HP_BAR_CHECK_INTERVAL,
                lambda x: x <= 0.1,
            ):
                logger.info("boss血条已消失")

                # 如果再检测到玩家血条，说明正常结算
                if check_normal_hp_bar(
                    image_settings.连续检测玩家血条次数,
                    BOSS_HP_BAR_CHECK_INTERVAL,
                    lambda x: x >= 0.8,
                ):
                    success_count += 1
                    continuous_fail_count = 0
                    need_refresh_checkpoint = True
                    logger.success("已检测到玩家的血条，本轮结算成功")

                    start_next_round()
                    break
                # 如果没有检测到玩家血条，说明灭了
                else:
                    logger.info("未检测到玩家的血条，本轮团灭")
                    continuous_fail_count += 1
                    break

            time.sleep(BOSS_HP_BAR_CHECK_INTERVAL)


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        ...
    except Exception as e:
        logger.critical(e)
        logger.info("程序已停止，请检查日志文件")
        _ = input("按回车键退出...")
