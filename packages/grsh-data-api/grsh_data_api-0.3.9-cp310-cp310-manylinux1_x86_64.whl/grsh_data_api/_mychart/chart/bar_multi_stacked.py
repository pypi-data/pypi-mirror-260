from grsh_data_api._mychart.base import GMPL, plt
from grsh_data_api._mychart.chart.line_multi import ChartLineMulti


class GmplBarMultiStacked(GMPL):
    def _plot(self):
        data = self.element.data
        _, ax = plt.subplots()
        for i, col in enumerate(data):
            if i == 0:
                ax.bar(
                    range(data.shape[0]),
                    data[col],
                    color=self.chart_color[i],
                    label=data.columns[i])
            else:
                ax.bar(
                    range(data.shape[0]),
                    data[col],
                    bottom=data.iloc[:, :i].sum(axis=1),
                    color=self.chart_color[i],
                    label=data.columns[i])

            # self.set_title(ax, param['title'])

        self._current_ax1 = ax


class ChartBarMultiStacked(ChartLineMulti):
    name = "bar_multi_stacked"
    desc = "柱状堆积图"
    num = "N"
    chart_type = "bar"
    gmpl_class = GmplBarMultiStacked
