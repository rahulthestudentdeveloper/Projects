import cv2
import numpy as np
import torchxrayvision as xrv


def preprocess_image(image):
    """
    Preprocess a PIL image for TorchXRayVision.
    """
    image = np.array(image)

    if image.ndim == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    image = cv2.resize(image, (224, 224))
    image = image.astype(np.float32)
    image = xrv.datasets.normalize(image, maxval=255)
    image = np.expand_dims(image, axis=0)
    return image