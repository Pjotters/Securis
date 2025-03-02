from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import numpy as np
import cv2

class AzureIrisDetector:
    def __init__(self):
        # Vervang met je eigen Azure credentials
        self.vision_key = "your-key"
        self.vision_endpoint = "your-endpoint"
        
        self.vision_client = ComputerVisionClient(
            self.vision_endpoint,
            CognitiveServicesCredentials(self.vision_key)
        )

    def detect_and_process(self, image):
        # Convert naar het juiste formaat voor Azure
        _, img_encoded = cv2.imencode('.jpg', image)
        
        # Analyze met Azure Computer Vision
        result = self.vision_client.analyze_image_in_stream(
            img_encoded.tobytes(),
            visual_features=['Objects', 'Faces']
        )

        # Verwerk de resultaten
        if result.faces:
            face = result.faces[0]
            # Extract oog regio
            eye_roi = self.extract_eye_region(image, face)
            return self.process_iris(eye_roi) if eye_roi is not None else None
        
        return None

    def extract_features(self, iris_image):
        # Gebruik Azure's geavanceerde feature extractie
        processed_image = self.preprocess_for_azure(iris_image)
        
        # Get deep features via Azure's API
        features = self.vision_client.analyze_image_in_stream(
            processed_image,
            features=['Description', 'Objects']
        )
        
        # Convert Azure features naar numpy array
        return self.convert_azure_features_to_vector(features) 