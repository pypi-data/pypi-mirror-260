import pandas as pd
from grsh_data_api.util import Tool
from grsh_data_api._mychart.base import GMPL, mpl
from grsh_data_api._mychart.chart.line_season import ChartLineSeason


class GmplLineLunarSeason(GMPL):
    def _set_xtick(self, ax: mpl.axes.Axes = None):
        if not ax:
            ax = self._current_ax1
        ax.set_xlim([self.element.data.index[0], self.element.data.index[-1]])
        xtick_label = ['1月15日', '4月1日', '5月5日', '7月1日', '8月15日', '9月9日', '12月8日']
        xtick_name = ['正月十五', '四月初一', '端午', '七月初一', '中秋', '重阳', '腊八']
        xtick_pos = [index for index, value in enumerate(self.element.index) if value in xtick_label]
        ax.set_xticks(xtick_pos)
        ax.set_xticklabels(xtick_name)

    def _set_hline(self, ax: mpl.axes.Axes = None):
        if not ax:
            ax = self._current_ax1
        hline_pos = [index for index, value in enumerate(self.element.index)
                     if value in ['1月15日', '5月5日', '8月15日']]
        for pos in hline_pos:
            ax.axvline(pos, c="k", ls="--")

    def _plot(self):
        self._current_ax1 = self.element.data.plot(color=self.chart_color[:len(self.element.data.columns)][::-1])

        _data = self.element.data.iloc[:, -1]    # 最新一年度最后
        if len(_data[_data.notnull()]) == 1:
            self._current_ax1.lines[-1].set_marker('_')
            # self._current_ax1.lines[-1].set_markersize(40)

        self._set_hline()




class ChartLineLunarSeason(ChartLineSeason):
    name = "line_lunar_season"
    desc = "农历季节性图"
    num = "1"
    gmpl_class = GmplLineLunarSeason

    def prepare_data(self):
        lunar_date = self.element.config['solar_lunar_mapping']

        data = self._data_series[0].df
        self.element.info.append(self._data_series[0].get_info())

        # data = pd.DataFrame(data)
        # data['date'] = pd.to_datetime(data['date']).apply(lambda x: x.date())

        param = self.element.param

        data_df = data.copy()
        data_df = data_df.set_index('date')

        min_date = data_df.index.min()
        max_date = data_df.index.max()
        data_df = data_df.reindex(pd.date_range(start=min_date, end=max_date))
        data_df = data_df.fillna(method='ffill')

        data_df.index.name = 'date'
        data_df = data_df.reset_index()
        data_df['date'] = data_df['date'].apply(lambda x: x.date())
        merge_data = pd.merge(data_df, lunar_date, how='left', left_on='date', right_on='solar_date')

        spring_pos = [i for i in range(len(merge_data['lunar_day'])) if merge_data['lunar_day'].iloc[i] == '1月1日']
        spring_pos.append(0)
        spring_pos.append(len(merge_data['lunar_day']))
        spring_pos = sorted(spring_pos)

        lunar_date_lst = []
        for i in range(1, 13):
            for j in range(1, 31):
                lunar_date_1 = '{}月{}日'.format(i, j)
                lunar_date_lst.append(lunar_date_1)
            for j in range(1, 31):
                lunar_date_2 = '闰{}月{}日'.format(i, j)
                lunar_date_lst.append(lunar_date_2)

        lunar_lst = []
        for i in range(1, len(spring_pos)):
            tmp = merge_data.iloc[spring_pos[i - 1]: spring_pos[i]]
            year = tmp['lunar_year'].iloc[0]
            tmp = tmp.iloc[:, [1, 5]].set_index('lunar_day')
            tmp.columns = [year]
            tmp = tmp.reindex(lunar_date_lst)
            lunar_lst.append(tmp)

        lunar_df = pd.concat(lunar_lst, axis=1)
        if param and "season_year" in param:
            year_str = param["season_year"]
            try:
                year_lst = [int(v) for v in year_str.replace(" ", "").split(',')]
                lunar_df = lunar_df[year_lst]
            except Exception as e:
                raise Exception("invalid year input %s" % e)

        lunar_df = lunar_df.dropna(how='all')
        # lunar_df = lunar_df[lunar_df.columns[::-1]]
        _max_year = lunar_df.columns.max()
        for year in lunar_df.columns:
            if year != _max_year:
                lunar_df[year].fillna(method='ffill', inplace=True)
            else:
                lunar_df = Tool.df_fill_to_end(lunar_df, year)

        lunar_df.index.name = "date"
        lunar_df.columns = [str(v) for v in lunar_df.columns]

        lunar_df = lunar_df.reset_index()
        # lunar_df.columns = ['date'] + sorted([v for v in lunar_df.columns if v != 'date'], reverse=True)
        self.data = Tool.df2list(lunar_df)
        self.element.index = list(lunar_df['date'])
        lunar_df = lunar_df.set_index("date")
        lunar_df.index = range(len(lunar_df))
        self.element.data = lunar_df
