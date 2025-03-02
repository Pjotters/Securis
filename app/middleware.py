from functools import wraps
from flask import request, jsonify
from app.auth_service import auth_service

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token ontbreekt'}), 401
            
        user_id = auth_service.verify_token(token)
        if not user_id:
            return jsonify({'message': 'Ongeldige token'}), 401
            
        return f(*args, **kwargs)
    return decorated 