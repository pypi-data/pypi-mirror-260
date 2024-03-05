import pandas as pd
from grsh_data_api.util import Tool
from grsh_data_api._mychart.base import Chart, GMPL, mpl
from grsh_data_api._mychart.util import strategy_xtick_label_cut


class GmplLineSeason(GMPL):
    def _set_xtick(self, ax: mpl.axes.Axes = None, rotation: int = None):
        if not ax:
            ax = self._current_ax1
        ax.set_xlim([self.element.data.index[0], self.element.data.index[-1]])
        if len(self.element.index) < 10:
            loc = range(len(self.element.index))
            label = list(self.element.index)
        else:
            loc, label = strategy_xtick_label_cut(self.element.index, self.element.info[0])
        ax.set_xticks(loc)
        ax.set_xticklabels(label)

    def _plot(self):
        self._current_ax1 = self.element.data.plot(
            color=self.chart_color[::-1]
        )

        _data = self.element.data.iloc[:, -1]    # 最新一年度最后
        if len(_data[_data.notnull()]) == 1:
            self._current_ax1.lines[-1].set_marker('_')
            # self._current_ax1.lines[-1].set_markersize(40)


'''
class GechartLineSeason(GECHART):
    def plot(self):
        # title = self.get_title_text()
        xaxis = [str(v) for v in self.element.index]
        # s = [list(self.element.data[self.element.data.columns[i]]) for i in range(len(self.element.data.columns))]
        s = []

        for i, name in enumerate(self.element.data.columns):
            _t = self.element.data[name].copy()
            _t = _t.fillna('')
            s.append(dict(type='line', data=list(_t), name=str(name), color=self._config_color(i)))

        option = dict(
            title=dict(text=self.element.info[0]['name'], left="center"),
            xAxis=dict(data=xaxis),
            series=s,    # [dict(type='line', data=v['serie'], name=v['name']) for v in s],

            legend=dict(),

            yAxis=dict(axisLine=dict(show=True), axisTick=dict(show=True)),
            tooltip=dict(
                trigger='axis',
                axisPointer=dict(type='line')
            ),
            dataZoom=[
                dict(type='inside', start=0, end=100),
                dict(start=0, end=100)
            ]
        )

        option_json = json.dumps(option, ensure_ascii=False)
        self.option = option_json
        self.template = ECHART_TEMPLATE.substitute(OPTION_JSON=option_json)
'''


class ChartLineSeason(Chart):
    num = "1"
    desc = "季节性图"
    name = "line_season"
    is_season = True
    gmpl_class = GmplLineSeason

    def prepare_data(self):
        param = self.element.param
        assert len(self._data_series) == 1

        data = self._data_series[0].df
        self.element.info.append(self._data_series[0].get_info())

        #data = pd.DataFrame(data)
        #data['date'] = pd.to_datetime(data['date']).apply(lambda x: x.date())

        data_df = data.copy()
        data_df['year'] = data_df['date'].apply(lambda x: x.year)
        data_df['day'] = data_df['date'].apply(lambda x: format(x, '%m-%d'))

        data_lst = []
        if param and "season_start_date" in param:
            season_start_date = param["season_start_date"]
            season_max_year = data_df['year'].max()
            season_min_year = data_df['year'].min()
            for i in range(season_min_year - 1, season_max_year + 1):
                s_date = pd.to_datetime("{}-{}".format(i, season_start_date)).date()
                e_date = pd.to_datetime("{}-{}".format(i + 1, season_start_date)).date()

                # tmp_df = data_df.query("date>=@s_date and date<@e_date")    # cython not support
                tmp_df = data_df[data_df['date'].apply(lambda x:  s_date <= x <= e_date)]

                tmp_df = tmp_df.drop(['year', 'date'], axis=1)
                tmp_df = tmp_df.set_index('day')
                # tmp_df.columns = ["{}-{}".format(str(i)[-2:], str(i + 1)[-2:])]
                tmp_df.columns = ["{}/{}".format(str(i), str(i + 1)[-2:])]  # 年份格式设置
                data_lst.append(tmp_df)
            season_data = pd.concat(data_lst, axis=1)
            season_month = [i for i in range(1, 13)]
            season_day = [i for i in range(1, 32)]
            s_month = s_date.month
            s_day = s_date.day
            s_month_order = season_month[(s_month - 1):] + season_month[:(s_month - 1)]
            s_month_order.append(s_month)
            s_day_order = season_day[(s_day - 1):]
            e_day_order = season_day[:(s_day - 1)]

            date_lst = []
            for index, value in enumerate(s_month_order):
                if index == 0:
                    for j in s_day_order:
                        date_lst.append("{}-{}".format(str(value).zfill(2), str(j).zfill(2)))
                elif index == 12:
                    for j in e_day_order:
                        date_lst.append("{}-{}".format(str(value).zfill(2), str(j).zfill(2)))
                else:
                    for j in range(1, 32):
                        date_lst.append("{}-{}".format(str(value).zfill(2), str(j).zfill(2)))
            season_data = season_data.reindex(date_lst)
        else:
            for year, year_data in data_df.groupby('year'):
                year_data = year_data.drop(['year', 'date'], axis=1)
                year_data = year_data.set_index('day')
                year_data.columns = [year]
                data_lst.append(year_data)
            season_data = pd.concat(data_lst, axis=1).sort_index()

        season_data.columns = [str(v) for v in season_data.columns]

        if param and "season_year" in param:
            year_str = param["season_year"]
            try:
                year_lst = year_str.replace(" ", "").split(',')
                year_lst = [v for v in year_lst]
                season_data = season_data[year_lst]
            except Exception as e:
                raise Exception("invalid year input %s" % e)

        season_data = season_data.dropna(how='all')
        season_data = season_data.dropna(how='all', axis=1)
        # season_data = season_data[season_data.columns[::-1]]    # 按照年度顺序，最新的年度最后绘制，更清晰点

        # 填充
        _max_year = season_data.columns.max()
        for year in season_data.columns:
            if year != _max_year:
                season_data[year].fillna(method='ffill', inplace=True)
            else:
                season_data = Tool.df_fill_to_end(season_data, year)

        season_data.index.name = "date"
        season_data = season_data.reset_index()

        self.data = Tool.df2list(season_data)

        self.element.index = list(season_data['date'])
        season_data = season_data.set_index("date")
        if not (self.element.param and 'skip_set_xtick' in self.element.param):
            season_data.index = range(len(season_data))
        self.element.data = season_data
