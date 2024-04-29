import threading
import time
from contextlib import contextmanager


def stop_loop(condition: threading.Condition):
    with condition:
        # 程序操作
        condition.notify()


def loop_with_timeout(condition: threading.Condition, timeout):
    with condition:
        if condition.wait(timeout):
            # 未超时
            ...
        else:
            # 超时
            ...


@contextmanager
def timeout(seconds):
    condition = threading.Condition()
    t = threading.Thread(target=stop_loop, args=(condition,))
    t.start()
    yield condition
    t.join(seconds)
    if t.is_alive():
        t.join()
        raise TimeoutError
