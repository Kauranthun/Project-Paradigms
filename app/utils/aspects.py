import time
import functools
from flask import request
from flask_login import current_user

stats = {
    "request_count": 0,
    "total_time": 0.0
}

def measure_performance(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        stats["request_count"] += 1
        stats["total_time"] += duration
        
        print(f"[PERF] {func.__name__} : {duration:.4f}s")
        return result
    return wrapper

def log_action(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user = current_user.username if (hasattr(current_user, 'is_authenticated') and current_user.is_authenticated) else "Anonyme"
        print(f"[LOG] {user} | {request.path}")
        return func(*args, **kwargs)
    return wrapper