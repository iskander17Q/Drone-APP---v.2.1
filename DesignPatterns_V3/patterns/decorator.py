"""Decorator: добавляет дополнительное логирование/временные метки к операциям анализа."""
from functools import wraps
import time


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[Timed] {func.__name__} took {end-start:.3f}s")
        return result

    return wrapper


def logged(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[Log] Calling {func.__name__} with args={args} kwargs={kwargs}")
        return func(*args, **kwargs)

    return wrapper
