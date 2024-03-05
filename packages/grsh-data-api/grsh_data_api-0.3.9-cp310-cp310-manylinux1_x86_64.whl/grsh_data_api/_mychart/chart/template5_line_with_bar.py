from grsh_data_api._mychart.base import GMPL
from grsh_data_api._mychart.chart.line_multi import ChartLineMulti


class GmplTemplate5LineWithBar(GMPL):
    def plot(self):
        data = self.element.data
        data_num = len(self.element.data.columns)

        ax1 = data[data.columns[:-1]].plot(color=self.chart_color)
        self._current_ax1 = ax1
        ax2 = ax1.twinx()
        ax2.bar(data.index, data[data.columns[-1]],
                color=self.chart_color[-1],
                label=data.columns[-1],
                align='center',
                alpha=0.5)
        ax2.spines['top'].set_visible(False)

        handles, labels = ax1.get_legend_handles_labels()
        handles2, labels2 = ax2.get_legend_handles_labels()
        labels2 = [i + ':右轴' for i in labels2]
        ax1.legend(handles + handles2,
                   labels + labels2,
                   loc='upper center',
                   frameon=False,
                   bbox_to_anchor=(0.5, 1.12),
                   fontsize=self.element.config['font_size_legend'])

        self._set_general()
        self._set_xtick()
        self._save_base64()


class ChartTemplate5LineWithBar(ChartLineMulti):
    name = "template5_line_with_bar"
    desc = "模板5:折线图+右轴柱状"
    num = "N"
    gmpl_class = GmplTemplate5LineWithBar
