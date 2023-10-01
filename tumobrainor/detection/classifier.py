from pathlib import Path
from keras.models import load_model
from detection.preprocessing import get_preprocessed_image
from src.constants import MODEL_PATH
import numpy as np

class Classifier:
    def __init__(self) -> None:
        self.model = load_model(MODEL_PATH)

    def classify(self, filepath: Path) -> int:
        image = get_preprocessed_image(filepath)
        prediction = self.model.predict(np.expand_dims(image, axis=0))
        return np.argmax(prediction[0])
