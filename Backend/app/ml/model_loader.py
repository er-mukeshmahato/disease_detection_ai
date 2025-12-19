import os
import tensorflow as tf
import hashlib
import gdown
from dotenv import load_dotenv
from filelock import FileLock

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

# --------------------------------------------------
# Model fingerprint (safe)
# --------------------------------------------------
def model_fingerprint(model):
    w = model.weights[0].numpy()
    return hashlib.md5(w.tobytes()).hexdigest()

# --------------------------------------------------
# Drive-ONLY Production Model Loader
# --------------------------------------------------
def model_load():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, "VGG16_drive.keras")
    LOCK_PATH = MODEL_PATH + ".lock"

    DRIVE_URL = os.getenv("DRIVE_URL")
    if not DRIVE_URL:
        raise EnvironmentError("❌ DRIVE_URL not found in .env")

    print("⬇️ Loading model from Google Drive (source of truth)")

    # 🔒 Prevent parallel downloads
    with FileLock(LOCK_PATH):

        # ❗ Always refresh from Drive
        if os.path.exists(MODEL_PATH):
            os.remove(MODEL_PATH)

        gdown.download(
            DRIVE_URL,
            MODEL_PATH,
            quiet=False,
            fuzzy=True
        )

        if not os.path.isfile(MODEL_PATH):
            raise RuntimeError("❌ Model download failed")

    print("🧠 Loading TensorFlow model...")

    model = tf.keras.models.load_model(
        MODEL_PATH,
        compile=False
    )

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    print("✅ Model loaded from Drive")
    print("🔐 API model fingerprint:", model_fingerprint(model))

    return model
