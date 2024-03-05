from grsh_data_api._mychart.base import GMPL, plt
from grsh_data_api._mychart.chart.line_multi import ChartLineMulti


class GmplLineMultiYaxis(GMPL):
    def plot(self):
        data = self.element.data

        fig, ax = plt.subplots()
        self._current_ax1 = ax

        param = self.element.param
        inverty = []
        if param and 'inverty' in param:
            try:
                inverty = [int(v.strip()) - 1 for v in param['inverty'].split(",")]
            except:
                pass

        line_lst = []
        for i in range(data.shape[1]):
            if i == 0:
                twinx = ax
            else:
                twinx = ax.twinx()

            line, = twinx.plot(data.iloc[:, i],
                               color=self.chart_color[i],
                               label=data.columns[i] if i not in inverty else data.columns[i] + "(倒序)")
            line_lst.append(line)

            twinx.tick_params(axis='y', color=line.get_color(), labelcolor=line.get_color())
            twinx.spines['top'].set_visible(False)
            if i > 1:
                twinx.spines['right'].set_position(('axes', 1 + 0.1 * (i - 1)))
            if i in inverty:
                twinx.invert_yaxis()

        plt.legend(handles=line_lst, loc='upper center', frameon=False,
                   bbox_to_anchor=(0.5, 1.12), fontsize=9)

        config = self.element.config
        plt.subplots_adjust(
            left=config['left'],
            right=config['right'],
            top=config['top'],
            bottom=config['bottom'],
        )


        self._set_datasource(ax)
        self._set_xtick(ax)
        self._set_hline_area(ax)
        self._save_base64()


class ChartLineMultiYaxis(ChartLineMulti):
    name = "line_multi_yaxis"
    desc = "多Y轴折线图"
    num = "N"
    gmpl_class = GmplLineMultiYaxis
