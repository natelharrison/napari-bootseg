import numpy as np
from skimage.feature import blob_doh

def predict_roi(image: np.ndarray) -> np.ndarray:
    image_shape = image.shape
    fake_labels = np.random.randint(0, 10, size=image_shape, dtype=np.uint8)
    return fake_labels

