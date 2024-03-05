from __future__ import annotations

import lightningchart
from lightningchart import conf, Themes
from lightningchart.charts import GeneralMethods, TitleMethods, ChartWithLUT, Chart
from lightningchart.instance import Instance


class GaugeChart(GeneralMethods, TitleMethods, ChartWithLUT):
    """Gauge charts indicate where your data point(s) falls over a particular range."""

    def __init__(
            self,
            start: int | float = None,
            end: int | float = None,
            value: int | float = None,
            angle_interval_start: int | float = 225,
            angle_interval_end: int | float = -45,
            thickness: int | float = 50,
            theme: Themes = Themes.White,
            title: str = None,
            license: str = None
    ):
        """A Gauge Chart with a single solid colored slice.

        Args:
            start (int | float): Start scale value.
            end (int | float): End scale value.
            value (int | float): Value of the gauge.
            angle_interval_start (int | float): Start angle of the gauge in degrees.
            angle_interval_end (int | float): End angle of the gauge in degrees.
            thickness (int | float): Thickness of the gauge.
            theme (Themes): Theme of the chart.
            title (str): Title of the chart.
            license (str): License key.
        """
        instance = Instance()
        Chart.__init__(self, instance)
        self.instance.send(self.id, 'gaugeChart', {'theme': theme.value, 'license': license or conf.LICENSE_KEY})
        self.set_angle_interval(angle_interval_start, angle_interval_end)
        self.set_thickness(thickness)
        if title:
            self.set_title(title)
        if start and end:
            self.set_interval(start, end)
        if value:
            self.set_value(value)

    def set_angle_interval(self, start: int | float, end: int | float):
        """Set angular interval of the gauge in degrees.

        Args:
            start (int | float): Start angle of the gauge in degrees.
            end (int | float): End angle of the gauge in degrees.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setAngleInterval', {
            'start': start,
            'end': end
        })
        return self

    def set_interval(self, start: int | float, end: int | float):
        """Set scale interval of the gauge slice.

        Args:
            start (int | float): Start scale value.
            end (int | float): End scale value.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setGaugeInterval', {'start': start, 'end': end})
        return self

    def set_value(self, value: int | float):
        """Set value of gauge slice.

        Args:
            value (int | float): Numeric value.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setGaugeValue', {'value': value})
        return self

    def set_thickness(self, thickness: int | float):
        """Set thickness of the gauge.

        Args:
            thickness (int | float): Thickness of the gauge.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setThickness', {'thickness': thickness})
        return self

    def set_gauge_color(self, color: lightningchart.Color):
        """Set the color of the underlying gauge arc, not the value slice.

        Args:
            color (Color): Color of the gauge.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setGaugeColor', {'color': color.get_hex()})
        return self

    def set_slice_color(self, color: lightningchart.Color):
        """Set the color gauge value slice.

        Args:
            color (Color): Color of the slice.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setSliceFillStyle', {'color': color.get_hex()})
        return self

    def set_label_color(self, color: lightningchart.Color):
        """Set the color of gauge data label.

        Args:
            color (Color): Color of the label.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setDataLabelFillStyle', {'color': color.get_hex()})
        return self

    def set_label_font(
            self,
            size: int | float,
            family: str = "Segoe UI, -apple-system, Verdana, Helvetica",
            style: str = 'normal',
            weight: str = 'normal'
    ):
        """Set font of gauge data labels.

        Args:
            size (int | float): CSS font size. For example, 16.
            family (str): CSS font family. For example, 'Arial, Helvetica, sans-serif'.
            weight (str): CSS font weight. For example, 'bold'.
            style (str): CSS font style. For example, 'italic'

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setDataLabelFont', {
            'family': family,
            'size': size,
            'weight': weight,
            'style': style
        })
        return self

    def set_highlight(self, highlight: float | bool = 1.0):
        """If highlight animations are enabled (which is true by default), the transition will be animated.
        As long as the component is highlighted, the active highlight intensity will be animated continuously
        between 0 and the configured value.

        Args:
            highlight (float | bool): Boolean or number between 0 and 1, where 1 is fully highlighted.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setGaugeHighlight', {'highlight': highlight})
        return self

    def set_gauge_stroke(
            self,
            thickness: int | float,
            color: lightningchart.Color
    ):
        """Set stroke of gauge background.

        Args:
            thickness (int | float): Thickness of the slice border.
            color (Color): Color of the slice border.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setGaugeStrokeStyle', {'thickness': thickness, 'color': color.get_hex()})
        return self

    def set_auto_scaling(self, enabled: bool):
        """Set the Auto Scaling mode enabled or disabled.

        Args:
            enabled (bool): True - autofit is enabled, otherwise - False.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setAutoScaling', {'enabled': enabled})
        return self

    def set_interval_label_padding(self, padding: int | float):
        """Set padding between Gauge and interval labels in pixels.

        Args:
            padding (int | float): Number with pixel margin.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setIntervalLabelPadding', {'padding': padding})
        return self


class GaugeChartDashboard(GaugeChart):

    def __init__(
            self,
            instance: Instance,
            dashboard_id: str,
            column: int,
            row: int,
            colspan: int,
            rowspan: int):
        Chart.__init__(self, instance)
        self.instance.send(self.id, 'createGaugeChart', {
            'db': dashboard_id,
            'column': column,
            'row': row,
            'colspan': colspan,
            'rowspan': rowspan
        })
