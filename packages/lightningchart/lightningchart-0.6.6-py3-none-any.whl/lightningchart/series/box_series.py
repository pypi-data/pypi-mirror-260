from __future__ import annotations

from lightningchart.charts import Chart
from lightningchart.ui.axis import Axis
from lightningchart.series import Series2D, Series


class BoxSeries(Series2D):
    """Series type for visualizing data groups through quartiles."""

    def __init__(
            self,
            chart: Chart,
            x_axis: Axis = None,
            y_axis: Axis = None
    ):
        Series.__init__(self, chart)
        self.instance.send(self.id, 'boxSeries2D', {
            'chart': self.chart.id,
            'xAxis': x_axis,
            'yAxis': y_axis
        })

    def add(
            self,
            start: int | float,
            end: int | float,
            median: int | float,
            lower_quartile: int | float,
            upper_quartile: int | float,
            lower_extreme: int | float,
            upper_extreme: int | float
    ):
        """Add new figure to the series.

        Args:
            start (int | float): Start x-value.
            end (int | float): End x-value.
            median (int | float): Median y-value.
            lower_quartile (int | float): Lower quartile y-value.
            upper_quartile (int | float): Upper quartile y-value.
            lower_extreme (int | float): Lower extreme y-value.
            upper_extreme (int | float): Upper extreme y-value.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'addBox2D', {
            'start': start,
            'end': end,
            'median': median,
            'lowerQuartile': lower_quartile,
            'upperQuartile': upper_quartile,
            'lowerExtreme': lower_extreme,
            'upperExtreme': upper_extreme
        })
        return self

    def add_multiple(self, data: list[dict]):
        """Add multiple figures to the series.

        Args:
            data: list of {start, end, median, lowerQuartile, upperQuartile, lowerExtreme, upperExtreme} objects

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'addMultipleBox2D', {'data': data})
        return self
