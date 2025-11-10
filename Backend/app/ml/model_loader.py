import os
import gdown
from tensorflow.keras.models import load_model as keras_load_model

def load_model():
    """
    Loads the trained chest disease detection model.
    If it's not found locally, it will be downloaded from Google Drive.
    """

    # ✅ Your Google Drive shareable link
    DRIVE_URL = "https://drive.google.com/uc?id=129E9m8ZRFObII6l2DfrLiMNLlYw7Ltig"

    # ✅ Model will be saved inside the same folder as this file
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, "chest_disease_model.h5")

    # ✅ Download the model only if it doesn’t exist
    if not os.path.exists(MODEL_PATH):
        print("🔽 Downloading model from Google Drive...")
        gdown.download(DRIVE_URL, MODEL_PATH, quiet=False)
        print("✅ Model downloaded successfully.")
    else:
        print("⚡ Model already exists locally — using cached version.")

    # ✅ Load the model
    print("🧠 Loading TensorFlow model...")
    model = keras_load_model(MODEL_PATH)
    print("✅ Model loaded and ready to use.")

    return model
