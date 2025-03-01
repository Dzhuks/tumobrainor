import flet
from detection.classifier import Classifier
from flet import Page, padding
from src.constants import DB_PATH, MRI_DIR, Color
from src.data_store import CSVDataStore
from src.tumobrainor import TumobrainorApp


def main(page: Page):
    classifier = Classifier()
    page.title = "Tumobrainor"
    # page.scroll = "auto"
    page.padding = padding.only(left=10, top=20)
    page.bgcolor = Color.GUNMETAL_DARK
    page.update()

    tumobrainor = TumobrainorApp(page, CSVDataStore(DB_PATH), classifier)
    tumobrainor.initialize()


flet.app(target=main, assets_dir=MRI_DIR)
