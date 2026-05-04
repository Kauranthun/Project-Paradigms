import time
import functools
from flask import request
from flask_login import current_user

# ASPECT 1 : Performance Monitoring
def measure_performance(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        print(f"[PERF] L'action '{func.__name__}' a mis {duration:.4f}s")
        return result
    return wrapper

# ASPECT 2 : Action Logging
def log_action(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user = current_user.username if (hasattr(current_user, 'is_authenticated') and current_user.is_authenticated) else "Anonyme"
        print(f"[LOG] Utilisateur: {user} | Route: {request.path} | Méthode: {request.method}")
        return func(*args, **kwargs)
    return wrapper