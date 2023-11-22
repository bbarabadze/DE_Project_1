import os
from typing import Callable
from datetime import datetime
from time import perf_counter


def log_error(message: str) -> None:
    """
    Logs error with timestamp to "error_log.txt" file
    :param message: Error message
    :return: None
    """
    with open("error_log.txt", "a") as f:
        f.write(f"{datetime.now()}: Error - {message}\n")


def check_paths_exist(*paths: str) -> None:
    """
    Checks if paths exist in operating system, if not, raises error and logs it
    :param paths: One or more path string
    :return: None
    """
    print("Checking input files and folders...")

    for path in paths:

        if not os.path.exists(path):
            err_message = f'"{path}" doesn\'t exist'
            log_error(err_message)
            raise IOError(err_message)

    print("Checking completed. All files and folders exist\n")


def timer(message: str) -> Callable:
    """
    Decorator factory function, returns a decorator function
    :param message: User-defined message which will be printed after running decorated function
    :return: Decorator function
    """
    def decorator(fn: Callable) -> Callable:
        """
        Decorator function which measures the running time of a decorated function
        :param fn: Function to be decorated
        :return: Decorated function
        """
        def inner(*args, **kwargs):
            """
            Wrapper function, in which a decorated function will run
            :param args: Positional parameters of a decorated function
            :param kwargs: Keyword-only parameters of a decorated function
            :return: Result of a decorated function
            """
            start_time = perf_counter()

            result = fn(*args, **kwargs)

            end_time = perf_counter() - start_time

            print(f"\n{message}")
            print(f"{end_time:.2f} seconds")

            return result

        return inner

    return decorator
