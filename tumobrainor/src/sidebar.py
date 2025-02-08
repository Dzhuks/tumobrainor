from typing import TYPE_CHECKING

from flet import (
    AnimationCurve,
    Container,
    CrossAxisAlignment,
    Icon,
    NavigationRail,
    NavigationRailDestination,
    NavigationRailLabelType,
    Page,
    Row,
    UserControl,
    animation,
    colors,
    icons,
    transform,
)
from src.constants import Color

if TYPE_CHECKING:
    from src.app_layout import AppLayout


class Sidebar(UserControl):
    def __init__(self, app_layout: "AppLayout", page: Page):
        super().__init__()
        self.app_layout = app_layout
        self.page = page

        self.indicator = Container(
            bgcolor=Color.PERSIAN_PINK,
            width=3,
            height=40,
            offset=transform.Offset(0, 0),
            animate_offset=animation.Animation(500, AnimationCurve.BOUNCE_OUT),
        )
        self.top_nav_items = [
            NavigationRailDestination(
                # label="Обнаружить",
                icon_content=Icon(icons.IMAGE_SEARCH, color=colors.BLACK),
                selected_icon=icons.IMAGE_SEARCH_OUTLINED,
            ),
            NavigationRailDestination(
                # label="Информация",
                icon_content=Icon(icons.INFO, color=colors.BLACK),
                selected_icon=icons.INFO_OUTLINED,
            ),
            NavigationRailDestination(
                # label="Статистика",
                icon_content=Icon(icons.QUERY_STATS, color=colors.BLACK),
                selected_icon=icons.QUERY_STATS_ROUNDED,
            ),
        ]
        self.top_nav_rail = NavigationRail(
            min_width=30,
            height=500,
            selected_index=0,
            label_type=NavigationRailLabelType.ALL,
            # group_alignment=-0.9,
            on_change=self.top_nav_change,
            destinations=self.top_nav_items,
            bgcolor=Color.GUNMETAL_DARK,
        )

    def build(self):
        self.view = Row(
            [
                self.indicator,
                self.top_nav_rail,
            ],
            spacing=0,
            expand=True,
            vertical_alignment=CrossAxisAlignment.START,
        )
        return self.view

    def top_nav_change(self, e):
        self.app_layout.change_view(e.control.selected_index)
        self.top_nav_rail.selected_index = e.control.selected_index * 1.70
        self.indicator.offset.y = e.control.selected_index
        self.indicator.update()
        self.update()
