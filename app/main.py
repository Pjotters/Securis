from flask import Flask, request, jsonify, render_template
import numpy as np
from app.detectors.improved_detector import ImprovedIrisDetector
from app.utils.db import IrisDB
from app.api_security import rate_limit
import base64
import cv2
import os
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from app.detectors.azure_iris_detector import AzureIrisDetector
from app.utils.logger import SecurityLogger
from app.detectors.enhanced_free_detector import EnhancedFreeDetector
from app.auth_service import AuthService

app = Flask(__name__, 
    template_folder=os.path.abspath('app/templates'),
    static_folder=os.path.abspath('app/static'))
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://pjotters.github.io"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Initialize beide detectoren
iris_detector = EnhancedFreeDetector()
backup_detector = ImprovedIrisDetector()
db = IrisDB()
auth_service = AuthService()
logger = SecurityLogger()

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Iris Scanner API"}
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/api/register-iris', methods=['POST'])
@rate_limit
def register_iris():
    try:
        data = request.json
        user_id = data.get('user_id')
        image_data = data.get('image')

        # Decodeer en verwerk de afbeelding
        img_bytes = base64.b64decode(image_data.split(',')[1])
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Detecteer en extraheer features
        iris = iris_detector.detect_and_process(img)
        if iris is not None:
            features = iris_detector.extract_features(iris)
            db.add_iris(user_id, features)
            return jsonify({'success': True, 'message': 'Iris geregistreerd'})
        
        return jsonify({'success': False, 'message': 'Geen iris gedetecteerd'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/verify-iris', methods=['POST'])
@rate_limit
def verify_iris():
    try:
        data = request.json
        image_data = data.get('image')

        # Decodeer en verwerk de afbeelding
        img_bytes = base64.b64decode(image_data.split(',')[1])
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Detecteer en extraheer features
        iris = iris_detector.detect_and_process(img)
        if iris is None:
            return jsonify({
                'success': False, 
                'message': 'Geen iris gedetecteerd'
            })

        # Extract features en vergelijk met database
        features = iris_detector.extract_features(iris)
        match = db.find_matching_iris(features)
        
        return jsonify({
            'success': True,
            'authorized': match is not None,
            'message': 'Iris herkend' if match else 'Iris niet herkend'
        })

    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Verificatie fout: {str(e)}'
        })

@app.route('/api/login-with-iris', methods=['POST'])
@rate_limit
def login_with_iris():
    try:
        data = request.json
        image_data = data.get('image')
        
        # Decodeer en verwerk de afbeelding
        img_bytes = base64.b64decode(image_data.split(',')[1])
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Iris verificatie (zoals in verify_iris)
        iris = iris_detector.detect_and_process(img)
        if iris is None:
            return jsonify({
                'success': False,
                'message': 'Geen iris gedetecteerd'
            })
            
        features = iris_detector.extract_features(iris)
        user_id = db.find_matching_iris(features)
        
        if user_id:
            logger.log_login_attempt(
                user_id=user_id,
                success=True,
                method='iris',
                ip=request.remote_addr
            )
            # Genereer auth token
            token = auth_service.create_auth_token(user_id)
            return jsonify({
                'success': True,
                'token': token,
                'user_id': user_id
            })
            
        logger.log_login_attempt(
            user_id='unknown',
            success=False,
            method='iris',
            ip=request.remote_addr
        )
        return jsonify({
            'success': False,
            'message': 'Gebruiker niet herkend'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/backup-login', methods=['POST'])
@rate_limit
def backup_login():
    try:
        data = request.json
        backup_code = data.get('backup_code')
        
        # Controleer backup code in database
        user = db.find_user_by_backup_code(backup_code)
        if user:
            token = auth_service.create_auth_token(user['user_id'])
            return jsonify({
                'success': True,
                'token': token
            })
            
        return jsonify({
            'success': False,
            'message': 'Ongeldige backup code'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port) 