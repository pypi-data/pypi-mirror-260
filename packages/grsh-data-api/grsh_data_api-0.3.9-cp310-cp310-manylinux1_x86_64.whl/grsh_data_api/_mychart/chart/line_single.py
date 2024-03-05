from grsh_data_api.util import Tool
from grsh_data_api._mychart.base import GMPL, Chart, mpl


class GmplLineSingle(GMPL):
    def _set_legend_position(self, ax: mpl.axes.Axes = None):
        if not ax:
            ax = self._current_ax1
        if ax.legend_:
            ax.legend_.remove()

    def _plot(self):
        ax = self.element.data.plot(color=self.chart_color)
        ax.set_xlim([self.element.data.index[0], self.element.data.index[-1]])
        self._current_ax1 = ax


class ChartLineSingle(Chart):
    name = "line_single"
    desc = "单折线图"
    num = "1"
    gmpl_class = GmplLineSingle

    def prepare_data(self):
        assert len(self._data_series) == 1

        param = self.element.param

        data = self._data_series[0].df
        self.element.info = [self._data_series[0].get_info(), ]
        self.element.index = list(data["date"])

        data.columns = ['date', self.info[0]['name']]
        self.data = Tool.df2list(data)

        data = data.set_index("date")
        if not ( param and 'skip_set_xtick' in param):
            data.index = range(len(data))
        data.columns = ['value']
        self.element.data = data
