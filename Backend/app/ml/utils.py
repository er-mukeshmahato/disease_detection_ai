import numpy as np
from PIL import Image
import io

def is_xray(image_bytes):
    """Basic check to reject non-X-ray images."""
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img_array = np.array(img)

    # Check grayscale-like image
    r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]
    color_diff = np.mean(np.abs(r - g) + np.abs(r - b))
    if color_diff > 15:
        return False

    # Check contrast
    gray = img.convert("L")
    contrast = np.std(np.array(gray))
    if contrast < 10:
        return False

    return True

def preprocess_image(image_bytes, target_size=(224, 224)):
    """Preprocess image before prediction."""
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize(target_size)
    img_array = np.expand_dims(np.array(img) / 255.0, axis=0)
    return img_array
