from __future__ import annotations
from lightningchart.charts import Chart
from lightningchart.instance import Instance
from lightningchart.series import Series


class ZoomBandChart(Chart):
    """Chart that is attached to a single Axis of a ChartXY."""

    def __init__(
            self,
            instance: Instance,
            chart_id: str,
            dashboard_id: str,
            column_index: int,
            column_span: int,
            row_index: int,
            row_span: int,
    ):
        Chart.__init__(self, instance)
        self.instance.send(self.id, 'zoomBandChart', {
            'db': dashboard_id,
            'chart': chart_id,
            'column_index': column_index,
            'column_span': column_span,
            'row_index': row_index,
            'row_span': row_span,
        })

    def add_series(self, series: Series):
        """Add a series to the ZoomBandChart.

        Args:
            series (Series): Series to attach.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'zbcAdd', {'series': series.id})
        return self
