import pandas as pd
from grsh_data_api._mychart.base import Chart, GMPL, GECHART, mpl, plt
from grsh_data_api._mychart.chart.line_multi import ChartLineMulti


class GmplLineMultiXaxis(GMPL):
    def _set_general(self, ax: mpl.axes.Axes = None):
        # general
        if not ax:
            ax = self._current_ax1

        config = self.element.config
        param = self.element.param

        plt.subplots_adjust(
            left=config['left'],
            right=config['right'],
            top=config['top'],
            bottom=config['bottom'])
        ax.set_xlabel(None)

        self._set_datasource(ax)

    def _set_legend_position(self, ax: mpl.axes.Axes = None):
        pass

    def _set_xtick(self, ax: mpl.axes.Axes = None, rotation: int = None):
        pass

    def _plot(self):
        serie_lst = self.element.serie_lst    # self._handle_data()
        _, ax = plt.subplots()
        self._current_ax1 = ax

        line_lst = []
        for i, serie in enumerate(serie_lst):
            _df = serie.df.set_index('date')
            if i == 0:
                twiny = ax
            else:
                twiny = ax.twiny()
            line, = twiny.plot(_df.index, _df, color=self.chart_color[i], label=_df.columns[0])
            line_lst.append(line)
            # twiny.xaxis.label.set_color(self.chart_color[i])
            twiny.tick_params(axis='x', colors=self.chart_color[i])
            if i>1:
                 twiny.spines['top'].set_position(('axes', 1+0.1*(i-1)))

        loc = self.element.param.get("legend_loc", None)

        plt.legend(
            handles=line_lst,
            loc= loc if loc else 'best',
            frameon=False,
            fontsize=self.element.config['font_size_legend'])


class ChartLineMultiXaxis(ChartLineMulti):
    name = "line_multi_xaxis"
    desc = "多X轴折线图"
    num = "N"
    gmpl_class = GmplLineMultiXaxis
