from functools import wraps
from flask import request, jsonify
import time

class RateLimiter:
    def __init__(self, limit=5, window=60):
        self.limit = limit
        self.window = window
        self.requests = {}

    def is_allowed(self, ip):
        current_time = time.time()
        if ip not in self.requests:
            self.requests[ip] = []
        
        # Verwijder oude verzoeken
        self.requests[ip] = [req_time for req_time in self.requests[ip] 
                           if current_time - req_time < self.window]
        
        if len(self.requests[ip]) >= self.limit:
            return False
            
        self.requests[ip].append(current_time)
        return True

rate_limiter = RateLimiter()

def rate_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not rate_limiter.is_allowed(request.remote_addr):
            return jsonify({'error': 'Te veel verzoeken, probeer het later opnieuw'}), 429
        return f(*args, **kwargs)
    return decorated_function 