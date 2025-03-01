import cv2
import numpy as np

class ImprovedIrisDetector:
    def __init__(self):
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
    def detect_and_process(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        eyes = self.eye_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(eyes) > 0:
            (x, y, w, h) = eyes[0]
            eye_region = gray[y:y+h, x:x+w]
            
            # Iris detectie met Hough Circles
            circles = cv2.HoughCircles(eye_region, cv2.HOUGH_GRADIENT, 1, 20,
                                     param1=50, param2=30, minRadius=10, maxRadius=30)
            
            if circles is not None:
                circles = np.uint16(np.around(circles))
                # Neem de eerste cirkel (iris)
                i = circles[0][0]
                # Extract iris region
                iris = eye_region[i[1]-i[2]:i[1]+i[2], i[0]-i[2]:i[0]+i[2]]
                return cv2.resize(iris, (64, 64))
        return None

    def extract_features(self, iris_image):
        # Eenvoudige feature extractie
        if iris_image is not None:
            # Gabor filter toepassen
            kernel = cv2.getGaborKernel((21, 21), 8.0, np.pi/4, 10.0, 0.5, 0, ktype=cv2.CV_32F)
            filtered = cv2.filter2D(iris_image, cv2.CV_8UC3, kernel)
            # Normaliseer features
            features = filtered.flatten() / 255.0
            return features
        return None 