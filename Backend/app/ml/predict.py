import numpy as np
from io import BytesIO
import tensorflow as tf


CLASS_NAMES = ['Covid', 'Normal', 'Pneumonia', 'Pneumothorax', 'Tuberculosis']

def predict_disease(model, file_bytes):

    # ----------------------------------
    # 1. LOAD IMAGE EXACTLY LIKE SCRIPT
    # ----------------------------------
    img = tf.keras.preprocessing.image.load_img(
        BytesIO(file_bytes),
        target_size=(224, 224),
        color_mode="rgb"
    )

    img_array = tf.keras.preprocessing.image.img_to_array(img)

    # ----------------------------------
    # 2. NORMALIZE (MATCH TRAINING)
    # ----------------------------------
    img_array = img_array / 255.0

    # ----------------------------------
    # 3. ADD BATCH DIMENSION
    # ----------------------------------
    x = np.expand_dims(img_array, axis=0)  # (1,224,224,3)
    


    print("min:", x.min())
    print("max:", x.max())
    print("mean:", x.mean())
    print("dtype:", x.dtype)
    print("shape:", x.shape)

    # ----------------------------------
    # 4. PREDICT
    # ----------------------------------
    preds = model.predict(x, verbose=0)[0]

    class_index = int(np.argmax(preds))
    confidence = float(preds[class_index])
    all_confidence = preds.tolist()

    print("API probs →", all_confidence)
    print("API predicted →", CLASS_NAMES[class_index])

    return x, class_index, confidence, all_confidence, img
