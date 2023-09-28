import random
import shutil
from typing import TYPE_CHECKING

from detection.classify import classify
from flet import (
    BorderSide,
    ButtonStyle,
    Column,
    Container,
    CrossAxisAlignment,
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    FontWeight,
    Image,
    ImageFit,
    MainAxisAlignment,
    MaterialState,
    Page,
    RoundedRectangleBorder,
    Row,
    Text,
    TextField,
    TextStyle,
    UserControl,
    colors,
    padding,
)
from src.constants import ASSETS_DIR, BRAIN_TUMOR_TYPES, MRI_DIR, TEXTS_DIR
from src.data_store import AbstractDataStore
from src.panels.base_panel import BasePanel

if TYPE_CHECKING:
    from src.app_layout import AppLayout


def get_tumor_desc(brain_tumor: str):
    with open(TEXTS_DIR / f"{brain_tumor}.txt", mode="r", encoding="utf-8") as f:
        contents = f.read()
        return contents


class DetectPanel(BasePanel):
    def __init__(
        self,
        app_layout: "AppLayout",
        app: UserControl,
        page: Page,
        store: AbstractDataStore,
        *args,
        **kwargs,
    ):
        super().__init__(app_layout, app, page, store, *args, **kwargs)

        self.file_picker = FilePicker(on_result=self.on_dialog_result)
        self.page.overlay.append(self.file_picker)
        self.page.update()

        # upload column
        self.image = Image(
            src=ASSETS_DIR / "default.png",
            width=400,
            height=400,
            fit=ImageFit.FILL,
        )
        self.imagename_field = TextField(
            label="Имя файла",
            value="default.png",
            autofocus=True,
            color=colors.GREY_200,
            label_style=TextStyle(color=colors.GREY_600),
        )
        self.buttons_row = Row(
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=CrossAxisAlignment.CENTER,
            width=400,
            controls=[
                ElevatedButton(
                    content=Container(
                        content=Column(
                            [
                                Text(value="Загрузить", size=24),
                                Text(value="снимок МРТ", size=16),
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            spacing=-15,
                        ),
                        padding=padding.all(10),
                    ),
                    style=ButtonStyle(
                        color={
                            MaterialState.HOVERED: colors.BLACK,
                            MaterialState.DEFAULT: colors.WHITE,
                        },
                        bgcolor=colors.GREEN_400,
                        overlay_color=colors.TRANSPARENT,
                        elevation={"pressed": 0, "": 1},
                        animation_duration=500,
                        side={
                            MaterialState.DEFAULT: BorderSide(1, colors.WHITE),
                            MaterialState.HOVERED: BorderSide(2, colors.WHITE),
                        },
                        shape=RoundedRectangleBorder(radius=20),
                    ),
                    width=195,
                    height=100,
                    on_click=self.file_picker.pick_files,
                ),
                ElevatedButton(
                    content=Container(
                        content=Column(
                            [
                                Text(value="Проверить", size=24),
                                Text(value="снимок", size=16),
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            spacing=-15,
                        ),
                        padding=padding.all(10),
                    ),
                    style=ButtonStyle(
                        color={
                            MaterialState.HOVERED: colors.BLACK,
                            MaterialState.DEFAULT: colors.WHITE,
                        },
                        bgcolor=colors.ORANGE_400,
                        overlay_color=colors.TRANSPARENT,
                        elevation={"pressed": 0, "": 1},
                        animation_duration=500,
                        side={
                            MaterialState.DEFAULT: BorderSide(1, colors.WHITE),
                            MaterialState.HOVERED: BorderSide(2, colors.WHITE),
                        },
                        shape=RoundedRectangleBorder(radius=20),
                    ),
                    width=195,
                    height=100,
                    on_click=self.classify_btn_clicked,
                ),
            ],
        )
        self.upload_col = Column(
            width=400,
            controls=[
                self.image,
                self.imagename_field,
                self.buttons_row,
            ],
        )

        # info column
        self.verdict = Text(
            size=36,
            color=colors.WHITE,
            weight=FontWeight.BOLD,
        )
        self.rec = Text(
            "Настоятельная просьба посетить врача-онколога",
            size=24,
            color=colors.RED,
            weight=FontWeight.BOLD,
        )
        self.desc_tumor = Text(
            size=16,
            color=colors.WHITE,
        )
        self.info_col = Column(
            controls=[
                self.verdict,
                self.rec,
                self.desc_tumor,
            ],
            width=700,
            alignment=MainAxisAlignment.START,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            visible=False,
        )

        self.controls = [
            Row(controls=[self.upload_col, self.info_col], spacing=40, vertical_alignment="start"),
        ]

    def on_dialog_result(self, e: FilePickerResultEvent):
        if not e.files:
            return
        brain_tumor_mri_file = e.files[0]
        try:
            destination_path = MRI_DIR / brain_tumor_mri_file.name
            shutil.copyfile(brain_tumor_mri_file.path, destination_path)
            self.image.src = destination_path
            self.imagename_field.value = brain_tumor_mri_file.name
            self.update()
        except IOError:
            pass

    def classify_btn_clicked(self, e):
        brain_tumor_type_index = classify(self.image.src)
        brain_tumor_type = BRAIN_TUMOR_TYPES[brain_tumor_type_index]

        record = {
            "filename": self.imagename_field.value,
            "brain_tumor_type": brain_tumor_type,
        }
        self.store.add_record(record)

        self._update_info_col(brain_tumor_type)
        self.update()

    def _update_info_col(self, brain_tumor_type: str):
        if brain_tumor_type == BRAIN_TUMOR_TYPES[0]:
            self.verdict.value = f"{brain_tumor_type} опухоль мозга"
            self.rec.text = "Рекомендуем ежегодно проходить скрининг"
            self.rec.color = colors.GREEN_300
        else:
            self.verdict.value = f"Обнаружена {brain_tumor_type}!"
            self.rec.text = "Настоятельная просьба посетить врача-онколога"
            self.rec.color = colors.RED_300
        self.desc_tumor.value = get_tumor_desc(brain_tumor_type)
        self.info_col.visible = True
