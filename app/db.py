import json
import os
import numpy as np

class SimpleDB:
    def __init__(self):
        self.db_file = 'iris_features.json'
        self.features = self.load_db()
    
    def load_db(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_db(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.features, f)
    
    def add_iris(self, user_id, features):
        self.features[user_id] = features.tolist()
        self.save_db()
    
    def verify_iris(self, features):
        min_distance = float('inf')
        matched_id = None
        
        for user_id, stored_features in self.features.items():
            dist = np.linalg.norm(features - np.array(stored_features))
            if dist < min_distance:
                min_distance = dist
                matched_id = user_id
                
        # Threshold voor verificatie
        return matched_id if min_distance < 0.3 else None 