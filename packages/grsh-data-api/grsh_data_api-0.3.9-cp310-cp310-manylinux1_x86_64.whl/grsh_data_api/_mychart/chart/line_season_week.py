import pandas as pd
from grsh_data_api.util import Tool
from grsh_data_api._mychart.base import Chart
from .line_season import GmplLineSeason


class GmplLineSeasonWeek(GmplLineSeason):
    pass


class ChartLineSeasonWeek(Chart):
    name = "line_season_week"
    desc = "季节性图（周度）"
    num = "1"
    is_season = True
    gmpl_class = GmplLineSeasonWeek

    def prepare_data(self):
        data = self._data_series[0].df
        self.element.info.append(self._data_series[0].get_info())

        data['date'] = pd.to_datetime(data['date'])
        data_df = data.copy()
        data_df = data_df.set_index('date')
        data_df = data_df.resample('W').last().sort_index()
        data_df.fillna(method='ffill', inplace=True)
        data_df = data_df.reset_index()
        data_df['year'] = data_df['date'].apply(lambda x: x.year)
        data_df['week_no'] = data_df['date'].apply(lambda x: '第{}周'.format(int(x.strftime("%W")) + 1))

        data_lst = []
        for year, year_data in data_df.groupby('year'):
            year_data = year_data.sort_values('date')
            year_data = year_data.set_index('week_no')
            year_data = year_data.drop(['year', 'date'], axis=1)
            year_data.columns = [year]
            data_lst.append(year_data)

        season_data = pd.concat(data_lst, axis=1)

        param = self.element.param
        if param and "season_year" in param:
            year_str = param["season_year"]
            try:
                year_lst = year_str.replace(" ", "").split(',')
                year_lst = [int(i) for i in year_lst]
                season_data = season_data[year_lst]
            except Exception as e:
                raise Exception("invalid year input %s" % e)

        season_data_index = ['第{}周'.format(i) for i in range(1, 54)]
        season_data = season_data.reindex(season_data_index).dropna(how='all')
        # season_data = season_data[season_data.columns[::-1]]

        season_data.index.name = "date"
        season_data = season_data.reset_index()

        self.data = Tool.df2list(season_data)

        self.element.index = list(season_data['date'])
        season_data = season_data.set_index("date")
        season_data.index = range(len(season_data))
        self.element.data = season_data
