from __future__ import annotations
from lightningchart.charts import Chart
from lightningchart.ui import UIEWithPosition, UIElement

VISIBILITY_MODES = ("always", "never", "whenDragged", "whenHovered", "whenHoveredOrDragged", "whenNotDragged")


def validate_visibility_mode(visibility_mode):
    if visibility_mode not in VISIBILITY_MODES:
        raise ValueError(
            f"Expected visibility_mode to be one of {VISIBILITY_MODES}"
            f", but got '{visibility_mode}'."
        )


class ChartMarker(UIEWithPosition):
    """Class for markers within a chart."""

    def __init__(self, chart: Chart, x: int, y: int):
        UIElement.__init__(self, chart)
        self.instance.send(self.id, 'addChartMarkerXY', {'chart': self.chart.id})
        if x and y:
            self.set_position(x, y)

    def set_visibility(self, visibility_mode: str = 'always'):
        """Set visibility mode for PointMarker. PointMarker is a visual that is displayed at the Cursors position.

        Args:
            visibility_mode (str): "always" | "never" | "whenDragged" | "whenHovered" |
                "whenHoveredOrDragged" | "whenNotDragged"

        Returns:
            The instance of the class for fluent interface.
        """
        validate_visibility_mode(visibility_mode)

        self.instance.send(self.id, 'setPointMarkerVisibility', {'visibility': visibility_mode})
        return self

    def set_grid_stroke_x_visibility(self, visibility_mode: str):
        """Set visibility mode for gridstroke X.

        Args:
            visibility_mode (str): "always" | "never" | "whenDragged" | "whenHovered" |
                "whenHoveredOrDragged" | "whenNotDragged"

        Returns:
            The instance of the class for fluent interface.
        """
        validate_visibility_mode(visibility_mode)

        self.instance.send(self.id, 'setGridStrokeXVisibility', {'visibilityMode': visibility_mode})
        return self

    def set_grid_stroke_y_visibility(self, visibility_mode: str):
        """Set visibility mode for gridstroke Y.

        Args:
            visibility_mode (str): "always" | "never" | "whenDragged" | "whenHovered" |
                "whenHoveredOrDragged" | "whenNotDragged"

        Returns:
            The instance of the class for fluent interface.
        """
        validate_visibility_mode(visibility_mode)

        self.instance.send(self.id, 'setGridStrokeYVisibility', {'visibilityMode': visibility_mode})
        return self

    def set_tick_marker_x_visibility(self, visibility_mode: str):
        """Set visibility mode for tickMarker X.

        Args:
            visibility_mode (str): "always" | "never" | "whenDragged" | "whenHovered" |
                "whenHoveredOrDragged" | "whenNotDragged"

        Returns:
            The instance of the class for fluent interface.
        """
        validate_visibility_mode(visibility_mode)

        self.instance.send(self.id, 'setTickMarkerXVisibility', {'visibilityMode': visibility_mode})
        return self

    def set_tick_marker_y_visibility(self, visibility_mode: str):
        """Set visibility mode for tickMarker Y.

        Args:
            visibility_mode (str): "always" | "never" | "whenDragged" | "whenHovered" |
                "whenHoveredOrDragged" | "whenNotDragged"

        Returns:
            The instance of the class for fluent interface.
        """
        validate_visibility_mode(visibility_mode)

        self.instance.send(self.id, 'setTickMarkerYVisibility', {'visibilityMode': visibility_mode})
        return self
