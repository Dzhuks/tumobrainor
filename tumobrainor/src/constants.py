from enum import StrEnum
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets"
MRI_DIR = ASSETS_DIR / "mri"
TEXTS_DIR = ASSETS_DIR / "texts"

MODEL_PATH = BASE_DIR / "detection" / "models" / "tumobrainor_tensorflow.h5"

BRAIN_TUMOR_TYPES = ["Глиома", "Менингиома", "Не обнаружена", "Аденома гипофиза"]

# Database constants
DB_PATH = BASE_DIR / "records.csv"
DB_FIELDNAMES = ("Дата", "Файл", "Тип опухоли")
DEFAULT_SHOWN_RECORDS_NUMBER = 15


class Color(StrEnum):
    GUNMETAL_DARK = "#282c34"
    PERSIAN_PINK = "#ff79c6"
    PALE_VIOLET = "#bd93f9"
