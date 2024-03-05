from grsh_data_api._mychart.base import GMPL, mpl
from grsh_data_api._mychart.chart.line_single import ChartLineSingle


class GmplBarSingle(GMPL):
    def _set_legend_position(self, ax: mpl.axes.Axes = None):
        if not ax:
            ax = self._current_ax1
        if ax.legend_:
            ax.legend_.remove()

    def _plot(self):
        ax = self.element.data.plot.bar(color=self.chart_color)
        ax.set_xlim([-1, len(self.element.data)])
        self._current_ax1 = ax


class ChartBarSingle(ChartLineSingle):
    name = "bar_single"
    desc = "单柱状图"
    num = "1"
    chart_type = "bar"
    gmpl_class = GmplBarSingle
