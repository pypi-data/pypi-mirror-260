import time


def get_current_timestamp() -> int:
    return int(time.time() * 1000.0)
