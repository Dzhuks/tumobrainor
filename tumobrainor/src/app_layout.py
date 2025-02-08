from typing import Union

from detection.classifier import Classifier
from flet import Column, Control, CrossAxisAlignment, MainAxisAlignment, Page, Row, Text, UserControl
from src.data_store import AbstractDataStore
from src.panels.detect_panel import DetectPanel
from src.panels.info_panel import InfoPanel
from src.panels.stat_panel import StatPanel
from src.sidebar import Sidebar


class AppLayout(Row):
    def __init__(self, app: UserControl, page: Page, store: AbstractDataStore, classifier: Classifier, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.page = page
        self.store = store
        self.classifier = classifier
        self.sidebar = Sidebar(self, page)

        self.detect_view = DetectPanel(
            self,
            self.app,
            self.page,
            self.store,
            self.classifier,
            width=1100,
            alignment=MainAxisAlignment.START,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=20,
        )
        self.info_view = InfoPanel(
            self,
            self.app,
            self.page,
            self.store,
            width=1100,
            alignment=MainAxisAlignment.START,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=40,
        )
        self.stat_view = StatPanel(
            self,
            self.app,
            self.page,
            self.store,
            width=1100,
            alignment=MainAxisAlignment.START,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=40,
        )
        self._active_view: Control = Column(
            controls=[Text("Active view")],
            alignment="center",
            horizontal_alignment="center",
        )
        self.controls = [self.sidebar, self.active_view]
        self._set_view(self.detect_view)

    @property
    def active_view(self):
        return self._active_view

    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.update()

    def change_view(self, selected_index: int):
        if selected_index == 0:
            self._set_view(self.detect_view)
        elif selected_index == 1:
            self._set_view(self.info_view)
        elif selected_index == 2:
            self._set_view(self.stat_view)
            self.stat_view.update_visuals()

    def _set_view(self, view: Union[Row, Column]):
        self._active_view = view
        self.controls[-1] = self._active_view
        self.page.update()
