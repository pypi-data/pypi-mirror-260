from grsh_data_api._mychart.base import GMPL, mpl
from grsh_data_api._mychart.chart.template2_two_line_compare_area import ChartTemplate2TwoLineCompareArea

class GmplTemplate3TwoLineCompareBar(GMPL):
    def _set_legend_position(self, ax: mpl.axes.Axes = None):
        pass

    def _plot(self):
        data = self.element.data

        ax1 = data[data.columns[:2]].plot(color=self.chart_color)
        ax2 = ax1.twinx()
        ax2.bar(self.element.data.index,
                data['spread'],
                color=self.chart_color[2],
                label='spread',
                align='center',
                alpha=0.5)
        ax2.spines['top'].set_visible(False)

        # merge legend
        handles, labels = ax1.get_legend_handles_labels()
        handles2, labels2 = ax2.get_legend_handles_labels()
        labels2 = [i + ':右轴' for i in labels2]
        ax1.legend(handles + handles2,
                   labels + labels2,
                   loc='best',
                   frameon=False,
                   # bbox_to_anchor=(0.5, 1.12),
                   fontsize=self.element.config['font_size_legend'])

        self._current_ax1 = ax1


class ChartTemplate3TwoLineCompareBar(ChartTemplate2TwoLineCompareArea):
    name = "template3_two_line_compare_bar"
    desc = "模板3:折线图+右轴柱状差值"
    num = "2"
    gmpl_class =GmplTemplate3TwoLineCompareBar
