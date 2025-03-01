from flask import Flask, request, jsonify, render_template
import numpy as np
from improved_detector import ImprovedIrisDetector
from db import SimpleDB
import base64
import cv2
import os

app = Flask(__name__)
detector = ImprovedIrisDetector()
db = SimpleDB()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/api/register-iris', methods=['POST'])
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