import numpy as np
import tensorflow as tf
import cv2

# ---------------------------------------------------------
# GRAD-CAM
# ---------------------------------------------------------
LAST_CONV = "block5_conv3"  # Last conv layer for VGG16

def generate_gradcam(model, x, class_index):
    last_conv_layer = model.get_layer(LAST_CONV)

    grad_model = tf.keras.Model(
        inputs=model.inputs,
        outputs=[last_conv_layer.output, model.output]
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(x)
        # ✅ DO NOT squeeze (predictions shape = [1, num_classes])
        loss = predictions[:, class_index]

    grads = tape.gradient(loss, conv_outputs)

    # Global average pooling on gradients
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # Convert to numpy
    conv_outputs = conv_outputs[0].numpy()
    pooled_grads = pooled_grads.numpy()

    # Weight the convolution outputs
    heatmap = np.zeros(conv_outputs.shape[:2], dtype=np.float32)
    for i in range(conv_outputs.shape[-1]):
        heatmap += pooled_grads[i] * conv_outputs[:, :, i]

    # ReLU + normalize
    heatmap = np.maximum(heatmap, 0)
    heatmap /= (np.max(heatmap) + 1e-8)

    # Resize to input image size
    heatmap = cv2.resize(heatmap, (224, 224))
    heatmap = np.uint8(255 * heatmap)

    return heatmap



def overlay_heatmap(pil_img, heatmap):
    # Resize original image to match heatmap
    img = pil_img.resize((heatmap.shape[1], heatmap.shape[0]))
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Make sure heatmap has 3 channels
    heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    heatmap_color = cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)

    # Convert both to same dtype
    img = img.astype(np.uint8)
    heatmap_color = heatmap_color.astype(np.uint8)

    overlay = cv2.addWeighted(img, 0.6, heatmap_color, 0.4, 0)
    return overlay
