import pandas as pd
from grsh_data_api.util import Tool
from grsh_data_api._mychart.base import Chart, GMPL, mpl


class GmplLineTwinx(GMPL):
    def __init__(self, element: object):
        GMPL.__init__(self, element)
        self.element.config['right'] = 1

    def _set_legend_position(self, ax: mpl.axes.Axes = None):
        pass

    def _plot(self):
        ax1 = self.element.data[self.element.data.columns[:-1]].plot(
            color=self.chart_color)
        ax2 = self.element.data[self.element.data.columns[-1]].plot(
            ax=ax1,
            secondary_y=True,
            color=self.chart_color[len(self.element.data.columns)-1:],
            mark_right=False)

        ax2.spines['top'].set_visible(False)

        #self.set_title(ax1, 1.13)

        # merge legend
        handles, labels = ax1.get_legend_handles_labels()
        handles2, labels2 = ax2.get_legend_handles_labels()
        labels2 = [i + ':右轴' for i in labels2]
        if self.element.title is None:
            ax1.legend(handles + handles2,
                       labels + labels2,
                       loc='upper center',
                       frameon=False,
                       bbox_to_anchor=(0.5, 1.12),
                       fontsize=self.element.config['font_size_legend'])
        else:
            ax1.legend(handles + handles2,
                       labels + labels2,
                       # loc='upper center',
                       loc = 'best',
                       frameon=False,
                       bbox_to_anchor=(0.5, 1.05),
                       fontsize=self.element.config['font_size_legend'])

        self._current_ax1 = ax1
        self._current_ax2 = ax2


class ChartLineTwinx(Chart):
    name = "line_twinx"
    desc = "双轴图（最后指标Y轴）"
    num = "N"
    gmpl_class = GmplLineTwinx

    def prepare_data(self):
        result = []
        for item in self._data_series:
            data = item.df
            info = item.get_info()
            self.element.info.append(info)

            #data = pd.DataFrame(data)
            #data['date'] = pd.to_datetime(data['date']).apply(lambda x: x.date())

            name = info['name']
            if 'unit' in info and info['unit']:
                name += " (%s)" % info['unit']
            data.columns = ['date', name]
            result.append(data.set_index("date"))

        result = pd.concat(result, axis=1)
        result = result.sort_index()
        result.index.name = 'date'
        for column in result.columns:
            result = Tool.df_fill_to_end(result, column)
        result = result.reset_index()

        self.data = Tool.df2list(result)

        self.element.index = list(result['date'])
        result = result.set_index("date")
        result.index = range(len(result))
        self.element.data = result
