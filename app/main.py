from flask import Flask, request, jsonify # type: ignore
import cv2 # type: ignore
import numpy as np # type: ignore
from tensorflow.keras.models import load_model # type: ignore
import base64
import os

app = Flask(__name__)

# Controleer of het model bestaat voordat we het laden
model_path = 'iris_recognition_model.h5'
if os.path.exists(model_path):
    iris_model = load_model(model_path)
else:
    print(f"Waarschuwing: Model bestand niet gevonden op pad: {model_path}")
    iris_model = None

def preprocess_iris_image(image_data):
    # Decodeer base64 image
    img_bytes = base64.b64decode(image_data.split(',')[1])
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Detecteer de iris
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    eyes = eye_cascade.detectMultiScale(img, 1.3, 5)
    
    if len(eyes) > 0:
        (x, y, w, h) = eyes[0]
        iris = img[y:y+h, x:x+w]
        iris = cv2.resize(iris, (64, 64))
        return iris
    return None

@app.route('/api/verify-iris', methods=['POST'])
def verify_iris():
    if iris_model is None:
        return jsonify({
            'authorized': False,
            'message': 'Model niet beschikbaar'
        })
    
    data = request.json
    iris_image = preprocess_iris_image(data['image'])
    
    if iris_image is None:
        return jsonify({'authorized': False, 'message': 'Geen iris gedetecteerd'})
    
    # Voorspelling maken met het model
    prediction = iris_model.predict(np.array([iris_image]))
    
    # Hier zou je normaal gesproken de voorspelling vergelijken met je database
    authorized = prediction[0] > 0.5
    
    return jsonify({
        'authorized': authorized,
        'message': 'Toegang verleend' if authorized else 'Toegang geweigerd'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080))) 