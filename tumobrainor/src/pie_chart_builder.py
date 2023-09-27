import seaborn as sns
from flet import BoxShadow, FontWeight, PieChart, PieChartEvent, PieChartSection, TextStyle, colors


def generate_vivid_colors_hex(num_colors: int):
    sns.set_palette("bright")  # Set the color palette to "bright"
    colors = sns.color_palette(n_colors=num_colors)
    hex_colors = [sns.palettes.mpl.colors.rgb2hex(color) for color in colors]
    return hex_colors


class PieChartBuilder:
    def __init__(self):
        self.normal_radius = 170
        self.hover_radius = 190
        self.normal_title_style = TextStyle(size=12, color=colors.WHITE, weight=FontWeight.BOLD)
        self.hover_title_style = TextStyle(
            size=16,
            color=colors.WHITE,
            weight=FontWeight.BOLD,
            shadow=BoxShadow(blur_radius=2, color=colors.BLACK54),
        )

        self.chart = PieChart(
            sections_space=0,
            center_space_radius=0,
            on_chart_event=self.on_chart_event,
            expand=True,
        )

    def on_chart_event(self, e: PieChartEvent):
        for idx, section in enumerate(self.chart.sections):
            if idx == e.section_index:
                section.radius = self.hover_radius
                section.title_style = self.hover_title_style
            else:
                section.radius = self.normal_radius
                section.title_style = self.normal_title_style
        self.chart.update()

    def build(self, stat: list[dict]) -> PieChart:
        self.chart.sections = []
        vivid_colors = generate_vivid_colors_hex(len(stat))
        for i, data in enumerate(stat):
            self.chart.sections.append(
                PieChartSection(
                    data["value"],
                    title=f"{data['title']}\n{data['value']} случаев, {data['percent']}%",
                    title_style=self.normal_title_style,
                    color=vivid_colors[i],
                    radius=self.normal_radius,
                )
            )
        return self.chart
