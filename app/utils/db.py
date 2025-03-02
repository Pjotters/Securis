from pymongo import MongoClient
import numpy as np
from datetime import datetime

class IrisDB:
    def __init__(self):
        username = "Pieter"
        password = "PieterAPI"  # Vervang dit met je wachtwoord
        cluster_url = "securis.rjv0y.mongodb.net"
        
        connection_string = f"mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority&appName=Securis"
        self.client = MongoClient(connection_string)
        self.db = self.client.iris_scanner
        self.iris_collection = self.db.iris_features

    def add_iris(self, user_id, features, metadata=None):
        document = {
            "user_id": user_id,
            "features": features.tolist(),
            "created_at": datetime.utcnow(),
            "metadata": metadata or {}
        }
        self.iris_collection.insert_one(document)

    def find_matching_iris(self, query_features, threshold=0.85):
        # Zoek alle opgeslagen irissen
        stored_irises = self.iris_collection.find()
        
        best_match = None
        highest_similarity = threshold

        for iris in stored_irises:
            stored_features = np.array(iris['features'])
            similarity = self.calculate_similarity(query_features, stored_features)
            
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = iris

        return best_match['user_id'] if best_match else None

    @staticmethod
    def calculate_similarity(features1, features2):
        return np.dot(features1, features2) / (
            np.linalg.norm(features1) * np.linalg.norm(features2)
        ) 