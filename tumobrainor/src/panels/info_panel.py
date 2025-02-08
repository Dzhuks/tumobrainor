from typing import TYPE_CHECKING

from flet import (
    BorderSide,
    ButtonStyle,
    Column,
    Container,
    CrossAxisAlignment,
    OutlinedButton,
    Page,
    Row,
    Text,
    UserControl,
    border,
    colors,
    padding,
)
from src.constants import Color
from src.data_store import AbstractDataStore

if TYPE_CHECKING:
    from src.app_layout import AppLayout

from src.panels.base_panel import BasePanel

GENERAL_INFO = """
A brain tumor is a mass or growth of abnormal cells in your brain.

There are many different types of brain tumors. Some brain tumors are noncancerous (benign), and some are cancerous (malignant). 
Brain tumors can begin in your brain (primary brain tumors), or cancer can begin in other parts of your body and spread to your brain as secondary (metastatic) brain tumors. The growth rate of a brain tumor can vary greatly. The growth rate, as well as the location of the brain tumor, determines how it will affect the function of your nervous system.
Treatment options for brain tumors depend on the type of brain tumor, as well as its size and location.

Classification of tumors by disease progression:
○ Grade I — noncancerous growths that grow slowly.
○ Grade II — slow growth, but the growth is beginning to become cancerous, and cells become atypical.
○ Grade III — cancerous growths that grow quickly.
○ Grade IV — very rapid growth and aggressiveness of the growth, spreading to adjacent parts of the brain, compressing its parts.
"""

SYMPTOMS_INFO = """
Signs and symptoms of a brain tumor vary greatly and depend on the size, location, and growth rate of the brain tumor. Make an appointment with your doctor if you have persistent signs and symptoms that concern you.

Common signs and symptoms caused by brain tumors may include:
- Headaches that gradually become more frequent and more severe
- Unexplained nausea or vomiting
- Vision problems, such as blurred vision, double vision, or loss of peripheral vision
- Gradual loss of sensation or movement in an arm or leg
- Difficulty with balance and speech
- Feeling very tired
- Inability to follow simple commands
- Seizures, especially in those who have no history of seizures
- Hearing problems
"""

TREATMENT_INFO = """
Treatment of brain tumors, like all cancers, is a complex and quite expensive process. All measures carried out during the course of treatment can be divided into the following groups:
- Symptomatic therapy
- Surgical treatment
- Radiation therapy
- Radiosurgery
- Chemotherapy
- Cryosurgery
- Combined treatment methods (radiation and chemotherapy)

Often, radiation therapy becomes an effective treatment method before and after surgery, and sometimes it is an independent treatment when surgical removal of the brain tumor is not possible. In this case, doctors can stop the growth of the tumor.

To prevent brain tumors, you should:
- Get enough sleep and rest
- Avoid excessive alcohol consumption
"""

RISK_FACTORS_INFO = """
Unfortunately, the causes of brain tumors are still unknown, but there are risk factors that may increase the likelihood of developing this disease.

Risk factors include:
- Radiation exposure. People who have been exposed to a type of radiation have an increased risk of developing a brain tumor. Exposure can include radiation therapy used to treat cancer and radiation exposure.
- Family history of disease. A small portion of brain tumors occur in people with a family history of brain tumors or a family history of genetic syndromes that increase the risk of brain tumors.
"""

INFO_BLOCKS = [GENERAL_INFO, SYMPTOMS_INFO, TREATMENT_INFO, RISK_FACTORS_INFO]


class PurpleClickButton(OutlinedButton):
    def __init__(self, text: str, selected: bool = False, *args, **kwargs):
        super().__init__(
            text,
            style=ButtonStyle(
                color=colors.BLACK,  # Changed to black for white theme
                side=BorderSide(2, colors.GREEN_300),
            ),
            width=250,
            height=50,
            *args,
            **kwargs,
        )
        if selected:
            self.selected()

    def selected(self):
        self.style.bgcolor = Color.PALE_VIOLET

    def unselected(self):
        self.style.bgcolor = colors.WHITE  # Changed to white for white theme


class InfoPanel(BasePanel):
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

        self.button_col = Column(
            controls=[
                PurpleClickButton("General Information", selected=True, on_click=self.toggle_button, data=0),
                PurpleClickButton("Symptoms", on_click=self.toggle_button, data=1),
                PurpleClickButton("Treatment and Prevention", on_click=self.toggle_button, data=2),
                PurpleClickButton("Risk Factors", on_click=self.toggle_button, data=3),
            ],
            width=250,
            spacing=15,
        )
        self.info = Container(
            content=Text(
                GENERAL_INFO,
                color=colors.BLACK,  # Changed to black for white theme
                size=16,
                width=800,
                selectable=True,
            ),
            border=border.all(2, color=colors.GREY),
            padding=padding.only(top=0, bottom=20, right=20, left=20),
        )
        self.info_row = Row(
            controls=[self.button_col, self.info],
            vertical_alignment=CrossAxisAlignment.START,
            spacing=40,
            height=650,
        )
        self.controls = [
            Container(
                Text("Brain Tumors", size=32, color=colors.BLACK),  # Changed to black for white theme
            ),
            self.info_row,
        ]

    def toggle_button(self, e):
        for button in self.button_col.controls:
            button.unselected()
        e.control.selected()

        self.info.content = Text(
            INFO_BLOCKS[e.control.data],
            color=colors.BLACK,  # Changed to black for white theme
            size=16,
            width=800,
            selectable=True,
        )

        self.update()
