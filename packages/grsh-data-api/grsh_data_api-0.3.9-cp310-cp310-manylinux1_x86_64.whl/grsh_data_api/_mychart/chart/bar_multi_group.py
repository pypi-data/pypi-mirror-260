from grsh_data_api._mychart.base import GMPL, plt
from grsh_data_api._mychart.chart.line_multi import ChartLineMulti


class GmplBarMultiGroup(GMPL):
    def _plot(self, tick_step=1, group_gap=0.2, bar_gap=0):
        _, self._current_ax1 = plt.subplots()
        labels = len(self.element.data)
        ticks = [i * tick_step for i in range(labels)]

        group_num = self.element.data.shape[1]
        group_width = tick_step - group_gap
        bar_span = group_width / group_num
        bar_width = bar_span - bar_gap
        baseline_x = [i - (group_width - bar_span) / 2 for i in ticks]
        for index, col in enumerate(self.element.data):
            bar_pos = [i + index * bar_span for i in baseline_x]
            self._current_ax1.bar(bar_pos,
                                  self.element.data[col], bar_width,
                                  color=self.chart_color[index],
                                  label=self.element.data.columns[index])

        # self._current_ax1.set_xlim([-0.5, len(self.element.data)])

    # def _set_xtick(self, ax: mpl.axes.Axes = None, rotation: int = None):
    #     pass


class ChartBarMultiGroup(ChartLineMulti):
    name = "bar_multi_group"
    desc = "多组柱状图"
    num = "N"
    chart_type = "bar"
    gmpl_class = GmplBarMultiGroup

