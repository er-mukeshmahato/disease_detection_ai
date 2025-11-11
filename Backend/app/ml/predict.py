import numpy as np
from tensorflow.keras.preprocessing import image
from io import BytesIO
from PIL import Image

def predict_disease(model, file_bytes):
    """
    Predicts the disease class index and confidence score from an uploaded image.
    Returns:
        class_index (int): predicted class index
        confidence (float): model confidence (probability of the predicted class)
    """
    # Load and preprocess image
    img = Image.open(BytesIO(file_bytes)).convert("RGB")
    img = img.resize((224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0  # Normalize to [0,1]

    # Predict probabilities for each class
    preds = model.predict(x)
    
    # Get highest probability class
    class_index = np.argmax(preds, axis=1)[0]
    confidence = float(np.max(preds))  # convert np.float32 → regular float

    return class_index, confidence
