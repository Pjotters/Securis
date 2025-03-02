from flask import Flask, request, jsonify, render_template
import numpy as np
from app.detectors.improved_detector import ImprovedIrisDetector
from app.utils.db import SimpleDB
from app.api_security import rate_limit
import base64
import cv2
import os
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://pjotters.github.io"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
detector = ImprovedIrisDetector()
db = SimpleDB()

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
        iris = detector.detect_and_process(img)
        if iris is not None:
            features = detector.extract_features(iris)
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
        iris = detector.detect_and_process(img)
        if iris is not None:
            features = detector.extract_features(iris)
            user_id = db.verify_iris(features)
            if user_id:
                return jsonify({'authorized': True, 'user_id': user_id})
        
        return jsonify({'authorized': False, 'message': 'Toegang geweigerd'})

    except Exception as e:
        return jsonify({'authorized': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True) 