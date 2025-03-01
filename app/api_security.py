from functools import wraps
from flask import request, jsonify
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, calls=15, period=60):
        self.calls = calls  # aantal toegestane calls
        self.period = period  # periode in seconden
        self.timestamps = defaultdict(list)
    
    def is_allowed(self, key):
        now = time.time()
        self.timestamps[key] = [ts for ts in self.timestamps[key] if ts > now - self.period]
        if len(self.timestamps[key]) < self.calls:
            self.timestamps[key].append(now)
            return True
        return False

rate_limiter = RateLimiter()

def rate_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not rate_limiter.is_allowed(request.remote_addr):
            return jsonify({'error': 'Te veel verzoeken, probeer het later opnieuw'}), 429
        return f(*args, **kwargs)
    return decorated_function 