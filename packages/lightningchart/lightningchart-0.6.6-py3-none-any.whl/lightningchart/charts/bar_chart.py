from __future__ import annotations

import lightningchart
from lightningchart import conf, Themes
from lightningchart.charts import GeneralMethods, TitleMethods, Chart
from lightningchart.instance import Instance
from lightningchart.ui.axis import CategoryAxis, ValueAxis


class BarChart(GeneralMethods, TitleMethods):
    """Chart type for visualizing categorical data as Bars."""

    def __init__(
            self,
            data: list[dict] = None,
            vertical: bool = True,
            title: str = None,
            theme: Themes = Themes.White,
            license: str = None
    ):
        """Create a bar chart.

        Args:
            data: List of {category, value} entries.
            vertical (bool): If true, bars are aligned vertically. If false, bars are aligned horizontally.
            title (str): The title of the chart.
            theme (Themes): The theme of the chart.
            license (str): License key.
        """
        instance = Instance()
        Chart.__init__(self, instance)

        self.instance.send(self.id, 'barChart', {
            'theme': theme.value,
            'vertical': vertical,
            'license': license or conf.LICENSE_KEY
        })
        self.category_axis = CategoryAxis(self)
        self.value_axis = ValueAxis(self)
        if title:
            self.set_title(title)
        if data:
            self.set_data(data)

    def set_data(self, data: list[dict]):
        """Set BarChart data, or update existing bars.

        Args:
            data (list[dict]): List of {category, value} entries.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setData', {'data': data})
        return self

    def set_data_grouped(self, categories: list[str], data: list[dict]):
        """Set BarChart data, updating the visible bars.
        This method accepts data for a Grouped Bar Chart, displaying it as such.

        Args:
            categories (list[str]): List of categories as strings.
            data: List of { "subCategory": str, "values" list[int | float] } dictionaries.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setDataGrouped', {'categories': categories, 'data': data})
        return self

    def set_data_stacked(self, categories: list[str], data: list[dict]):
        """Set BarChart data, updating the visible bars.
        This method accepts data for a Stacked Bar Chart, displaying it as such.

        Args:
            categories (list[str]): List of categories as strings.
            data: List of { "subCategory": str, "values" list[int | float] } dictionaries.

        Returns:

        """
        self.instance.send(self.id, 'setDataStacked', {'categories': categories, 'data': data})
        return self

    def set_value_label_display_mode(self, display_mode: str = 'afterBar'):
        """Configure how value labels are displayed in the Bar Chart.

        Args:
            display_mode: "afterBar" | "insideBar" | "hidden"

        Returns:
            The instance of the class for fluent interface.
        """
        display_modes = ("afterBar", "insideBar", "hidden")
        if display_mode not in display_modes:
            raise ValueError(
                f"Expected display_mode to be one of {display_modes}"
                f", but got '{display_mode}'."
            )

        self.instance.send(self.id, 'setValueLabels', {'displayMode': display_mode})
        return self

    def set_value_label_color(self, color: lightningchart.Color):
        """Set the color of value labels.

        Args:
            color (Color): Color of the labels.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setValueLabelColor', {'color': color.get_hex()})
        return self

    def set_value_label_font_size(self, size: int | float):
        """Set the font size of value labels.

        Args:
            size (int | float): Font size of the labels.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setValueLabelFontSize', {'size': size})
        return self

    def set_sorting(self, mode: str):
        """Configure automatic sorting of bars.

        Args:
            mode: "disabled" | "ascending" | "descending" | "alphabetical"

        Returns:
            The instance of the class for fluent interface.
        """
        sorting_modes = ("disabled", "ascending", "descending", "alphabetical")
        if mode not in sorting_modes:
            raise ValueError(
                f"Expected mode to be one of {sorting_modes}"
                f", but got '{mode}'."
            )

        self.instance.send(self.id, 'setSorting', {'mode': mode})
        return self

    def set_label_fitting(self, enabled: bool):
        """Enable or disable automatic label fitting.

        Args:
            enabled (bool): If true, labels will not overlap.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setLabelFitting', {'enabled': enabled})
        return self

    def set_series_background_effect(self, enabled: bool = True):
        """Set theme effect enabled on component or disabled.

        Args:
            enabled (bool): Theme effect enabled.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setSeriesBackgroundEffect', {'enabled': enabled})
        return self

    def set_series_background_color(
            self,
            color: lightningchart.Color
    ):
        """Set chart series background color.

        Args:
            color (Color): Color of the series background.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setSeriesBackgroundFillStyle', {'color': color.get_hex()})
        return self

    def set_animation_category_position(self, enabled: bool):
        """Enable/disable animation of bar category positions. This is enabled by default.

        Args:
            enabled (bool): Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setAnimationCategoryPosition', {'enabled': enabled})
        return self

    def set_animation_values(self, enabled: bool):
        """Enable/disable animation of bar values. This is enabled by default.

        Args:
            enabled (bool): Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setAnimationValues', {'enabled': enabled})
        return self

    def set_bars_effect(self, enabled: bool):
        """Set theme effect enabled on component or disabled.

        Args:
            enabled (bool): Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setBarsEffect', {'enabled': enabled})
        return self

    def set_bars_margin(self, margin: int | float):
        """Set margin around each bar along category axis as percentage of the bar thickness.
        For example, 0.1 = on both left and right side of bar there is a 10% margin.
        Actual thickness of bar depends on chart size, but for 100 px bar that would be 10 px + 10 px margin.
        Valid value range is between [0, 0.49].

        Args:
            margin (int | float): Margin around each bar along category axis as percentage of bar thickness.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setBarsMargin', {'margin': margin})
        return self


class BarChartDashboard(BarChart):
    def __init__(
            self,
            instance: Instance,
            dashboard_id: str,
            column: int,
            row: int,
            colspan: int,
            rowspan: int
    ):
        Chart.__init__(self, instance)
        self.instance.send(self.id, 'createBarChart', {
            'db': dashboard_id,
            'column': column,
            'row': row,
            'colspan': colspan,
            'rowspan': rowspan
        })
