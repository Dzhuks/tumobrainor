from typing import TYPE_CHECKING

from flet import Column, Page, UserControl
from src.data_store import AbstractDataStore
from detection.classifier import Classifier

if TYPE_CHECKING:
    from src.app_layout import AppLayout


class BasePanel(Column):
    def __init__(
        self,
        app_layout: "AppLayout",
        app: UserControl,
        page: Page,
        store: AbstractDataStore,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.app_layout = app_layout
        self.app = app
        self.page = page
        self.store = store
