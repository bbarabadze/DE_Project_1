import os
from typing import Callable
from datetime import datetime
from time import perf_counter


def log_error(message: str) -> None:
    with open("error_log.txt", "a") as f:
        f.write(f"{datetime.now()}: Error - {message}\n")


def check_paths_exist(*paths: str) -> None:
    print("Checking input files and folders...")
    for path in paths:
        if not os.path.exists(path):
            err_message = f'"{path}" doesn\'t exist'
            log_error(err_message)
            raise IOError(err_message)
    print("Checking completed. All files and folders exist\n")


def timer(message: str) -> Callable:

    def decorator(fn: Callable) -> Callable:

        def inner(*args, **kwargs):

            start_time = perf_counter()
            result = fn(*args, **kwargs)
            end_time = perf_counter() - start_time
            print(f"\n{message}")
            print(f"{end_time:.2f} seconds")
            return result

        return inner

    return decorator
