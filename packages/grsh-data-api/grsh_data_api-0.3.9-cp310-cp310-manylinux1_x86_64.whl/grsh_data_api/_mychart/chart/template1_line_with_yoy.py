import pandas as pd
from grsh_data_api.util import Tool
from dateutil.relativedelta import relativedelta
from grsh_data_api._mychart.base import Chart, GMPL, mpl, plt


class GmplTemplate1LineWithYoy(GMPL):
    def __init__(self, element: object):
        GMPL.__init__(self, element)
        self.element.config['right'] = 0.9

    def _set_legend_position(self, ax: mpl.axes.Axes = None):
        if not ax:
            ax = self._current_ax2
        GMPL._set_legend_position(self, ax)

    def _plot(self):
        _, ax1 = plt.subplots()
        ax1.plot(self.element.data.index,
                 self.element.data['value'],
                 color=self.chart_color[0],
                 # label=self.element.data.columns[0]
                 )
        ax2 = ax1.twinx()
        ax2.fill_between(
            self.element.data.index, self.element.data['yoy'],
            0,
            color=self.chart_color[0] + [0.3, ],
            label='yoy %:右轴'
        )
        # self.data['yoy'].plot.bar(ax=ax2, label='yoy %:右轴', color=self.color_default[1])
        ax2.spines['top'].set_visible(False)

        self._current_ax1 = ax1
        self._current_ax2 = ax2


class ChartTemplate1LineWithYoy(Chart):
    name = "template1_line_with_yoy"
    desc = "模板1:折线图+右轴同比"
    num = "1"
    gmpl_class = GmplTemplate1LineWithYoy

    def prepare_data(self):
        data = self._data_series[0].df
        self.element.info.append(self._data_series[0].get_info())

        #data = pd.DataFrame(data)
        #data.columns = ['date', 'value']
        #data['date'] = pd.to_datetime(data['date']).apply(lambda x: x.date())

        last_year_data = data.copy()
        last_year_data['ndate'] = last_year_data['date'].apply(lambda x: x + relativedelta(years=1))
        last_year_data = last_year_data[last_year_data['ndate'] <= data['date'].max()]
        last_year_data = last_year_data[['ndate', 'value']]
        last_year_data.columns = ['date', 'last_year']

        data = data[data['date'] >= last_year_data['date'].min()]
        data = data.set_index('date')
        last_year_data = last_year_data.set_index('date')

        # result = pd.concat([data, last_year_data], axis=1)
        result = pd.merge(data, last_year_data, how='outer', left_index=True, right_index=True)
        result = result.sort_index()
        result['last_year'] = result['last_year'].fillna(method='ffill')
        result = result[result['value'].notnull()]
        result['yoy'] = (result['value'] / result['last_year'] - 1) * 100

        result = result[['value', 'yoy']]

        result.index.name = 'date'
        result = result.reset_index()

        self.data = Tool.df2list(result)

        self.element.index = list(result['date'])
        result = result.set_index("date")
        result.index = range(len(result))
        self.element.data = result
