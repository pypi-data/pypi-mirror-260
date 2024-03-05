import matplotlib.pyplot as plt
from .line_season import ChartLineSeason, GmplLineSeason


class GmplLineSeasonArea(GmplLineSeason):
    def _plot(self):
        season_line_num = 5

        param = self.element.param
        if param and 'season_line_num' in param:
            season_line_num = int(param['season_line_num'])
        columns = self.element.data.columns

        _, ax = plt.subplots()

        _max = self.element.data[columns[:-1]].max(axis=1)
        _min = self.element.data[columns[:-1]].min(axis=1)
        ax.fill_between(self.element.data.index,
                        y1=_max, y2=_min,
                        facecolor=self.chart_color[1],
                        alpha=0.2,
                        label='%s-%s' % (columns[0], columns[-1]))
        ax.set_xlim(self.element.data.index[0], self.element.data.index[-1])

        _data = self.element.data[columns[(len(columns) - min(len(columns), season_line_num)):]]
        _data.plot(color=self.chart_color[:len(_data.columns)][::-1], ax=ax)

        self._current_ax1 = ax

        _data = self.element.data.iloc[:, -1]    # 最新一年度最后
        if len(_data[_data.notnull()]) == 1:
            self._current_ax1.lines[-1].set_marker('_')
            # self._current_ax1.lines[-1].set_markersize(40)


class ChartLineSeasonArea(ChartLineSeason):
    num = "1"
    desc = "季节性图（面积）"
    name = "line_season_area"
    is_season = True
    gmpl_class = GmplLineSeasonArea
