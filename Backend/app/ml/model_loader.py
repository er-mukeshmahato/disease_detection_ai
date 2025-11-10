import os
from tensorflow.keras.models import load_model as keras_load_model

def load_model():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # main.py folder
    MODEL_PATH = os.path.join(BASE_DIR, "ml", "chest_disease_model.h5")

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")

    model = keras_load_model(MODEL_PATH)
    return model
