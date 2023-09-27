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
Опухоль мозга - это образование или рост аномальных клеток в вашем мозге.

Существует множество различных типов опухолей мозга. Некоторые опухоли мозга являются нераковыми (доброкачественными), а некоторые -раковыми (злокачественными).
Опухоли мозга могут зарождаться в мозге (первичные опухоли мозга), или рак может зародиться в других частях тела и распространиться на мозг в виде вторичных (метастатических) опухолей мозга. Скорость роста опухоли мозга может сильно варьироваться. Скорость роста, а также расположение опухоли мозга определяют, как она повлияет на работу вашей нервной системы.
Варианты лечения опухолей мозга зависят от типа опухоли мозга, а также от ее размера и расположения.

Классификация опухолей по степени развития болезни:
○ І степень — новообразования, не имеющие признаков злокачественности, которые растут медленно. 
○ ІІ степень — медленный рост, но новообразование уже начинает приобретать злокачественность,
клетки становятся атипичными.
○ ІІІ степень ― злокачественные образования, быстро растут.
○ ІѴ степень — очень быстрый рост и агрессивность новообразования, прорастание в соседние отделы мозга, сжатие его частей.
"""

SYMPTOMS_INFO = """
Признаки и симптомы опухоли мозга сильно варьируются и зависят от размера, расположения и скорости роста опухоли мозга. Запишитесь на прием к врачу, если у вас есть постоянные признаки и симптомы, которые вас беспокоят.

Общие признаки и симптомы, вызванные опухолями головного мозга, могут включать:
- Головные боли, которые постепенно становятся более частыми и более сильными
- Необъяснимая тошнота или рвота
- Проблемы со зрением, такие как помутнение зрения, двоение в глазах или потеря периферического зрения
- Постепенная потеря чувствительности или движения в руке или ноге
- Трудности с равновесием и речью
- Чувство сильной усталости
- Неспособность выполнять простые команды
- Судороги, особенно у тех, кто не страдает судорогами в прошлом
- Проблемы со слухом
"""

TREATMENT_INFO = """
Лечение опухолей головного мозга, как и всех онкологических заболеваний, — комплексное и довольно дорогостоящее мероприятие. Все мероприятия, проводимые в ходе курса лечения, можно разбить на следующие группы:
- Симптоматическая терапия
- Хирургическое лечение
- Лучевая терапия
- Радиохирургия
- Химиотерапия
- Криохирургия
- Методы комбинированного лечения (лучевая и химиотерапия)

Часто именно лучевая терапия становится действенным методом лечения до операции и после нее, а иногда она является самостоятельным средством лечения, когда иссечение опухоли головного мозга невозможно. В этом случае врачам удается остановить рост новообразования.

Чтобы предотвратить появление опухолей головного мозга, надо:
- достаточно спать и отдыхать
- избегать чрезмерного употребления алкоголя
"""

RISK_FACTORS_INFO = """
К сожалению, до сих пор неизвестны причины возникновения опухолей мозга, но есть факторы риска, которые могут повысить вероятность появления данной болезни.

К факторам риска относятся:
- Воздействие радиации. Люди, которые подверглись воздействию вида излучения, имеют повышенный Приск развития опухоли мозга. Воздействием может быть лучевая терапия, применяемая для лечения рака, и радиационное облучение.
- Семейная история заболеваний. Небольшая часть опухолей мозга возникает у людей с семейной историей опухолей мозга или семейной историей генетических синдромов, которые повышают риск развития опухолей мозга.
"""

INFO_BLOCKS = [GENERAL_INFO, SYMPTOMS_INFO, TREATMENT_INFO, RISK_FACTORS_INFO]


class PurpleClickButton(OutlinedButton):
    def __init__(self, text: str, selected: bool = False, *args, **kwargs):
        super().__init__(
            text,
            style=ButtonStyle(
                color=colors.WHITE,
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
        self.style.bgcolor = Color.GUNMETAL_DARK


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
                PurpleClickButton("Общая информация", selected=True, on_click=self.toggle_button, data=0),
                PurpleClickButton("Симптомы", on_click=self.toggle_button, data=1),
                PurpleClickButton("Лечение и профилактика", on_click=self.toggle_button, data=2),
                PurpleClickButton("Группы риска", on_click=self.toggle_button, data=3),
            ],
            width=250,
            spacing=15,
        )
        self.info = Container(
            content=Text(
                GENERAL_INFO,
                color=colors.WHITE,
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
                Text("Опухоли мозга", size=32, color=colors.WHITE),
            ),
            self.info_row,
        ]

    def toggle_button(self, e):
        for button in self.button_col.controls:
            button.unselected()
        e.control.selected()

        self.info.content = Text(
            INFO_BLOCKS[e.control.data],
            color=colors.WHITE,
            size=16,
            width=800,
            selectable=True,
        )

        self.update()
