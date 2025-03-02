import cv2
import numpy as np
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input

class EnhancedFreeDetector:
    def __init__(self):
        # ResNet50 voor feature extractie (gratis, voorgetraind)
        self.feature_extractor = ResNet50(
            weights='imagenet',
            include_top=False, 
            pooling='avg'
        )
        # Verbeterde eye detection
        self.eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_eye.xml'
        )
        
    def detect_and_process(self, image):
        # Check beeldkwaliteit
        if not self._check_image_quality(image):
            return None, "Beeldkwaliteit te laag"
            
        # Verbeterde voorbewerking
        processed = self._preprocess_image(image)
        
        # Detecteer ogen met verschillende parameters
        eyes = self._detect_eyes_multi_scale(processed)
        if not eyes:
            return None, "Geen oog gedetecteerd"
            
        # Neem beste oog ROI
        eye_roi = self._get_best_eye_roi(image, eyes)
        if eye_roi is None:
            return None, "Oog niet goed zichtbaar"
            
        # Iris segmentatie met verbeterde parameters
        iris_roi = self._segment_iris(eye_roi)
        if iris_roi is None:
            return None, "Iris niet gevonden"
            
        return iris_roi, "OK"

    def _preprocess_image(self, image):
        # Contrast verbetering
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        l = clahe.apply(l)
        enhanced = cv2.merge((l,a,b))
        return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)

    def _check_image_quality(self, image):
        # Check scherpte
        laplacian = cv2.Laplacian(image, cv2.CV_64F).var()
        if laplacian < 100:
            return False
            
        # Check helderheid
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        if brightness < 40 or brightness > 250:
            return False
            
        return True

    def _detect_eyes_multi_scale(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        eyes = []
        
        # Probeer verschillende parameters
        scale_factors = [1.1, 1.2, 1.3]
        min_neighbors_range = [3, 4, 5]
        
        for scale in scale_factors:
            for min_neighbors in min_neighbors_range:
                detected = self.eye_cascade.detectMultiScale(
                    gray,
                    scaleFactor=scale,
                    minNeighbors=min_neighbors,
                    minSize=(30, 30)
                )
                if len(detected) > 0:
                    eyes.extend(detected)
                    
        return eyes if eyes else None

    def extract_features(self, iris_image):
        # Voorbewerking
        iris_resized = cv2.resize(iris_image, (224, 224))
        iris_array = np.expand_dims(iris_resized, axis=0)
        iris_preprocessed = preprocess_input(iris_array)
        
        # Feature extractie
        features = self.feature_extractor.predict(iris_preprocessed)
        features = features.flatten()
        # L2 normalisatie voor betere matching
        features = features / np.linalg.norm(features)
        
        return features 