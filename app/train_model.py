import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# Model architectuur
def create_model():
    model = Sequential([
        # Convolutional layers
        Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
        MaxPooling2D(2, 2),
        
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        
        # Flatten en Dense layers
        Flatten(),
        Dense(64, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')
    ])
    
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    return model

# Dummy data genereren voor test doeleinden
def generate_dummy_data():
    # Maak 100 dummy iris afbeeldingen
    X = np.random.rand(100, 64, 64, 3)
    # Labels: 0 voor niet-geautoriseerd, 1 voor geautoriseerd
    y = np.random.randint(2, size=100)
    
    return X, y

def main():
    # Model maken
    model = create_model()
    
    # Dummy data genereren
    X, y = generate_dummy_data()
    
    # Model trainen
    model.fit(
        X, y,
        epochs=10,
        batch_size=32,
        validation_split=0.2
    )
    
    # Model opslaan
    model.save('iris_recognition_model.h5')
    print("Model opgeslagen als 'iris_recognition_model.h5'")

if __name__ == "__main__":
    main() 