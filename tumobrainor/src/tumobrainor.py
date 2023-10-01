from flet import Page, UserControl
from src.app_layout import AppLayout
from src.data_store import AbstractDataStore
from detection.classifier import Classifier


class TumobrainorApp(UserControl):
    def __init__(self, page: Page, store: AbstractDataStore, classifier: Classifier):
        self.page = page
        self.store = store
        self.classifier = classifier
        self.layout = AppLayout(
            self,
            self.page,
            self.store,
            self.classifier,
            tight=True,
            expand=True,
            vertical_alignment="start",
        )

    def initialize(self):
        self.page.add(self.layout)
        self.page.update()
