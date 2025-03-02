import cv2
import numpy as np
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input

class ImprovedIrisDetector:
    def __init__(self):
        # Laad het voorgetrainde model voor feature extractie
        self.feature_extractor = ResNet50(weights='imagenet', include_top=False, pooling='avg')
        # Laad de Haar Cascade voor iris detectie
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    def detect_and_process(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        eyes = self.eye_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(eyes) == 0:
            return None
            
        # Neem het grootste gedetecteerde oog
        eye_x, eye_y, eye_w, eye_h = max(eyes, key=lambda x: x[2] * x[3])
        eye_roi = image[eye_y:eye_y+eye_h, eye_x:eye_x+eye_w]
        
        # Voorbewerking van het oog
        eye_roi = cv2.resize(eye_roi, (224, 224))  # ResNet50 input size
        eye_roi = cv2.GaussianBlur(eye_roi, (5, 5), 0)
        
        # Iris segmentatie met Hough circles
        gray_roi = cv2.cvtColor(eye_roi, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(gray_roi, cv2.HOUGH_GRADIENT, 1, 20,
                                 param1=50, param2=30, minRadius=20, maxRadius=100)
                                 
        if circles is None:
            return None
            
        # Neem de meest waarschijnlijke iris
        circle = circles[0][0]
        center_x, center_y, radius = map(int, circle)
        
        # Knip de iris uit
        iris_roi = eye_roi[
            max(0, center_y-radius):min(224, center_y+radius),
            max(0, center_x-radius):min(224, center_x+radius)
        ]
        
        return iris_roi if iris_roi.size > 0 else None

    def extract_features(self, iris_image):
        # Voorbewerking voor ResNet50
        iris_resized = cv2.resize(iris_image, (224, 224))
        iris_array = np.expand_dims(iris_resized, axis=0)
        iris_preprocessed = preprocess_input(iris_array)
        
        # Extract features
        features = self.feature_extractor.predict(iris_preprocessed)
        # Normaliseer features
        features = features.flatten()
        features = features / np.linalg.norm(features)
        
        return features 