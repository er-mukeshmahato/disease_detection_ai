from tensorflow.keras.models import load_model as keras_load_model

def load_model(model_path: str):
    model = keras_load_model(model_path)
    return model
