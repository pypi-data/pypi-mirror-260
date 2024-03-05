from grsh_data_api._mychart.base import GMPL, mpl
from grsh_data_api._mychart.chart.line_single import ChartLineSingle


class GmplHist(GMPL):
    def _set_xtick(self, ax: mpl.axes.Axes = None, rotation: int = None):
        pass

    def _set_legend_position(self, ax: mpl.axes.Axes = None):
        if not ax:
            ax = self._current_ax1
        if 'legend_font_size_adjust' in self.element.param:
            _tmp = int(self.element.param['legend_font_size_adjust'])
            font_size = max(self.element.config['font_size_legend'] + _tmp, 6)
        else:
            font_size = self.element.config['font_size_legend']
        ax.legend(loc="best", frameon=False, fontsize=font_size)

    def _plot(self):
        data = self.element.data[self.element.data.columns[0]]
        start_date = min(self.element.index)
        end_date = max(self.element.index)
        start_date = format(start_date, "%Y%m%d")
        end_date = format(end_date, "%Y%m%d")

        ax = data.plot(kind='hist', bins='fd', color=self.chart_color, label=f"时间区间:{start_date}-{end_date}")
        latest_value = data.iloc[-1]
        quantile = round(len(data[data <= latest_value]) / len(data) * 100, 1)
        ax.axvline(latest_value, c="r", alpha=0.6, label=f"最新值:{round(latest_value, 2)},分位数:{quantile}%")
        self._current_ax1 = ax


class ChartHist(ChartLineSingle):
    name = "hist"
    desc = "直方图"
    num = "1"
    gmpl_class = GmplHist
