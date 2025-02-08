from pathlib import Path

import numpy as np
import tensorflow as tf
from detection.preprocessing import get_preprocessed_image
from keras.models import load_model
from src.constants import MODEL_PATH


class Classifier:
    def __init__(self) -> None:
        self.model = tf.keras.models.load_model(MODEL_PATH)

    def classify(self, filepath: Path) -> int:
        image = get_preprocessed_image(filepath)
        prediction = self.model.predict(np.expand_dims(image, axis=0))
        return np.argmax(prediction[0])
