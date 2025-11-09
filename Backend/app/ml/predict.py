import numpy as np
from tensorflow.keras.preprocessing import image
from io import BytesIO
from PIL import Image

def predict_disease(model, file_bytes):
    # Load image
    img = Image.open(BytesIO(file_bytes)).convert("RGB")
    img = img.resize((224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0  # normalize

    preds = model.predict(x)
    class_index = np.argmax(preds, axis=1)[0]
    return class_index
