from typing import TYPE_CHECKING

from flet import (
    Column,
    Container,
    CrossAxisAlignment,
    DataCell,
    DataColumn,
    DataRow,
    DataTable,
    Page,
    Row,
    ScrollMode,
    Slider,
    Text,
    UserControl,
    colors,
)
from src.constants import DEFAULT_SHOWN_RECORDS_NUMBER
from src.panels.base_panel import BasePanel
from src.pie_chart_builder import PieChartBuilder

if TYPE_CHECKING:
    from src.app_layout import AppLayout

from src.data_store import AbstractDataStore


class StatPanel(BasePanel):
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

        self.records_number_slider_text = Text(f"Количество строк: {DEFAULT_SHOWN_RECORDS_NUMBER}", color=colors.WHITE)
        self.records_number_slider = Slider(
            min=1,
            max=self.store.get_records_number(),
            value=DEFAULT_SHOWN_RECORDS_NUMBER,
            divisions=100,
            label="{value}",
            on_change=self.slider_change,
            data=DEFAULT_SHOWN_RECORDS_NUMBER,
        )
        self.records_number_cntr = Container(
            content=Column(
                controls=[self.records_number_slider_text, self.records_number_slider],
                spacing=-10,
            )
        )

        labels = ["Номер"] + self.store.get_labels()
        self.brain_tumor_data_table = DataTable(
            columns=[
                DataColumn(
                    Text(label, color=colors.WHITE, weight=700),
                )
                for label in labels
            ],
        )
        self._update_brain_tumor_data_table()
        self.brain_tumor_data_table_col = Column(
            [
                Row(
                    [Container(self.brain_tumor_data_table, bgcolor=colors.GREEN)],
                    scroll=ScrollMode.ALWAYS,
                )
            ],
            scroll=ScrollMode.ALWAYS,
        )

        self.pie_chart_builder = PieChartBuilder()
        self.chart = self.pie_chart_builder.build(self.store.get_stat(DEFAULT_SHOWN_RECORDS_NUMBER))

        self.controls = [
            Container(Text("История загрузок", size=32, color=colors.WHITE)),
            Row(
                controls=[
                    Column(controls=[self.records_number_cntr, self.brain_tumor_data_table_col]),
                    self.chart,
                ],
                height=600,
                vertical_alignment=CrossAxisAlignment.CENTER,
            ),
        ]

    def _get_slider_records_number(self):
        return int(round(self.records_number_slider.value))

    def _update_brain_tumor_data_table(self):
        self.brain_tumor_data_table.rows = []
        records_number = self._get_slider_records_number()
        records = self.store.get_records(records_number)

        for i, record in enumerate(records):
            values = [i + 1] + record
            self.brain_tumor_data_table.rows.append(
                DataRow(
                    cells=[DataCell(Text(value, color=colors.WHITE)) for value in values],
                )
            )

    def _update_pie_chart(self):
        stat = self.store.get_stat(self._get_slider_records_number())
        self.chart = self.pie_chart_builder.build(stat)

    def slider_change(self, e):
        self.records_number_slider_text.value = f"Количество строк: {self._get_slider_records_number()}"

        self.update_visuals()

    def update_visuals(self):
        self.records_number_slider.max = self.store.get_records_number()
        self._update_brain_tumor_data_table()
        self._update_pie_chart()
        self.update()
