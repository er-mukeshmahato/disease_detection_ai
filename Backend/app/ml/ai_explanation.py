import numpy as np
from PIL import Image
import requests
import io


# ================================
# DOWNLOAD HEATMAP (ROBUST)
# ================================
def load_heatmap(gradcam_url: str) -> np.ndarray:
    """Download and convert Grad-CAM image into a numpy array safely."""
    try:
        response = requests.get(gradcam_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ValueError(f"Failed to download Grad-CAM image: {e}")

    try:
        img = Image.open(io.BytesIO(response.content)).convert("RGB")
        arr = np.array(img)
    except Exception:
        raise ValueError("Downloaded file is not a valid image")

    if arr.size == 0:
        raise ValueError("Empty Grad-CAM heatmap image")

    return arr


# ================================
# HEATMAP FOCUS DETECTOR
# ================================
def determine_heatmap_focus(heatmap: np.ndarray) -> str:
    """
    Determine heatmap activation strength:
    weak / moderate / strong
    """
    # Convert to grayscale
    if heatmap.ndim == 3:
        heatmap_gray = np.mean(heatmap, axis=2)
    else:
        heatmap_gray = heatmap

    # Normalize to 0–1
    heatmap_norm = heatmap_gray / 255.0
    max_intensity = float(np.max(heatmap_norm))

    if max_intensity < 0.30:
        return "weak"
    elif max_intensity < 0.60:
        return "moderate"
    else:
        return "strong"


# ================================
# AI EXPLANATION GENERATOR
# ================================
def ai_explanation(pred_class: str, confidence: float, heatmap_focus: str) -> str:
    """
    Generate a clean, PDF-safe AI explanation.
    Confidence is assumed to be already in percentage (e.g. 72.99)
    """

    disease_explanations = {
        "Covid": (
            "The Grad-CAM highlights diffuse regions across both lungs. "
            "These patterns may correspond to ground-glass opacities "
            "commonly observed in COVID-19 cases."
        ),
        "Normal": (
            "The Grad-CAM shows low and evenly distributed activation, "
            "suggesting no focal abnormalities in the lung fields."
        ),
        "Pneumonia": (
            "The model highlights localized patchy regions, which may "
            "correspond to inflammatory consolidations typical of pneumonia."
        ),
        "Pneumothorax": (
            "Activation is concentrated near the lung periphery, "
            "which can be associated with lung collapse or air leakage."
        ),
        "Tuberculosis": (
            "The model focuses on upper lung zones and irregular structures, "
            "which are commonly associated with tuberculosis-related changes."
        ),
    }

    intensity_explanation = {
        "weak": (
            "Activation strength is weak, indicating subtle radiographic features "
            "had a limited influence on the model’s decision."
        ),
        "moderate": (
            "Moderate activation suggests the model identified noticeable but "
            "not highly pronounced disease-related patterns."
        ),
        "strong": (
            "Strong activation indicates the presence of clear radiographic "
            "patterns that strongly influenced the prediction."
        ),
    }

    explanation_text = (
        f"Prediction: {pred_class}\n"
        f"Confidence: {confidence * 100:.2f}%\n\n"
        f"{disease_explanations.get(pred_class, 'No class-specific explanation available.')}\n\n"
        f"{intensity_explanation.get(heatmap_focus, '')}"
    )

    return explanation_text
