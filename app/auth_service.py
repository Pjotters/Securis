from flask import session, redirect, url_for
import jwt
import os
from datetime import datetime, timedelta

class AuthService:
    def __init__(self):
        self.secret_key = os.environ.get('JWT_SECRET_KEY', 'your-secret-key')
        
    def create_auth_token(self, user_id):
        return jwt.encode(
            {'user_id': user_id},
            self.secret_key,
            algorithm='HS256'
        )
        
    def verify_token(self, token):
        try:
            data = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return data['user_id']
        except:
            return None

    def create_refresh_token(self, user_id):
        return jwt.encode(
            {
                'user_id': user_id,
                'exp': datetime.utcnow() + timedelta(days=30),
                'type': 'refresh'
            },
            self.secret_key,
            algorithm='HS256'
        )
        
    def refresh_auth_token(self, refresh_token):
        try:
            data = jwt.decode(refresh_token, self.secret_key, algorithms=['HS256'])
            if data['type'] != 'refresh':
                return None
                
            return {
                'token': self.create_auth_token(data['user_id']),
                'refreshToken': self.create_refresh_token(data['user_id'])
            }
        except:
            return None