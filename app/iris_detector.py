import dlib
import cv2
import numpy as np
from imutils import face_utils

class IrisDetector:
    def __init__(self):
        # Laad de dlib face detector en shape predictor
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        
    def detect_iris(self, image):
        # Convert naar grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detecteer gezichten
        faces = self.detector(gray)
        
        if len(faces) > 0:
            # Krijg facial landmarks
            shape = self.predictor(gray, faces[0])
            shape = face_utils.shape_to_np(shape)
            
            # Extraheer oog regio's
            left_eye = shape[36:42]
            right_eye = shape[42:48]
            
            # Bereken oog centra
            left_eye_center = left_eye.mean(axis=0).astype("int")
            right_eye_center = right_eye.mean(axis=0).astype("int")
            
            return left_eye_center, right_eye_center
            
        return None 