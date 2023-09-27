from flet import Page, UserControl
from src.app_layout import AppLayout
from src.data_store import AbstractDataStore


class TumobrainorApp(UserControl):
    def __init__(self, page: Page, store: AbstractDataStore):
        self.page = page
        self.store = store
        self.layout = AppLayout(
            self,
            self.page,
            self.store,
            tight=True,
            expand=True,
            vertical_alignment="start",
        )

    def initialize(self):
        self.page.add(self.layout)
        self.page.update()
