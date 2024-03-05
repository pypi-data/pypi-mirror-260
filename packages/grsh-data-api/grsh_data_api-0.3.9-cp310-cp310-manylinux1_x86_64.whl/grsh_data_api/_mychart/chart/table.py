import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
from grsh_data_api._mychart.base import GMPL, plt, mpl
from grsh_data_api._mychart.chart.line_single import ChartLineSingle


class GmplTable(GMPL):
    def _set_title(self, ax: mpl.axes.Axes = None, y: float = 0.9):
        GMPL._set_title(self, ax, y)

    def _set_general(self, ax: mpl.axes.Axes = None):
        # general
        if not ax:
            ax = self._current_ax1

        plt.subplots_adjust(
            left=self.element.config['left'],
            right=self.element.config['right'],
            top=self.element.config['top'],
            bottom=self.element.config['bottom'])


        self._set_datasource(ax)
        '''
        param = self.element.param
        if ('data_source' in param and param['data_source'] == 'T') or ('data_source' not in param):
            label_data_source = "资料来源: 国泰君安期货研究"
            for v in self.element.data_source:
                if v not in ('GTJAQH', '国泰君安期货'):
                    label_data_source += ", %s" % v
            ax.text(1.03, 0.1, label_data_source,
                    multialignment='center',
                    verticalalignment='bottom',
                    horizontalalignment='right',
                    fontsize=self.element.config['font_size_datasource'],
                    transform=ax.transAxes)
        '''

    def _plot(self):
        _, ax = plt.subplots()
        tab = plt.table(cellText=self.element.data.values.tolist(),
                        colLabels=self.element.data.columns,
                        rowLabels=self.element.index,
                        loc='center',
                        cellLoc='center',
                        rowLoc='center')
        tab.auto_set_font_size(False)
        tab.set_fontsize(10)
        tab.auto_set_column_width(self.element.data.columns)
        tab.scale(1, 2)
        plt.axis('off')

        self._current_ax1 = ax


class ChartTable(ChartLineSingle):
    name = "table"
    desc = "数据表格"
    num = "1"
    gmpl_class = GmplTable

    def prepare_data(self):
        def _cal_yoy(df, col):
            series = df[col].dropna()
            max_date = series.index.max()
            last_date = max_date - datetime.timedelta(days=365)
            yoy_date = series[series.index >= last_date].index.min()
            yoy_value = series.loc[yoy_date]
            return yoy_value

        data = self._data_series[0].df
        self.element.info.append(self._data_series[0].get_info())

        #data = pd.DataFrame(data)
        #data.columns = ['date', 'value']
        #data['date'] = pd.to_datetime(data['date']).apply(lambda x: x.date())
        data = data.sort_values("date")

        last_year_data = data.copy()
        last_year_data['ndate'] = last_year_data['date'].apply(lambda x: x + relativedelta(years=1))
        last_year_data = last_year_data[last_year_data['ndate'] <= data['date'].max()]
        last_year_data = last_year_data[['ndate', 'value']]
        last_year_data.columns = ['date', 'last_year']

        data = data[data['date'] >= last_year_data['date'].min()]
        data = data.set_index('date')
        last_year_data = last_year_data.set_index('date')

        result = pd.merge(data, last_year_data, how='outer', left_index=True, right_index=True)
        result = result.sort_index()
        result['last_year'] = result['last_year'].fillna(method='ffill')
        result = result[result['value'].notnull()]
        result['yoy'] = result['value'] - result['last_year']
        result['mom'] = result['value'] - result['value'].shift(1)
        result['yoy'] = result['yoy'].apply(lambda x: '{:+}'.format(round(x, 2)) if x > 0 else round(x, 2))
        result['mom'] = result['mom'].apply(lambda x: '{:+}'.format(round(x, 2)) if x > 0 else round(x, 2))
        result = result[['value', 'mom', 'yoy']]
        result.columns = ['原始数据', '环比变动', '同比变动']
        result = result.sort_index(ascending=False)
        result = result.iloc[:5]

        result = result.reset_index()
        self.element.index = list(result['date'])
        result = result.set_index("date")
        result.index = range(len(result))
        self.element.data = result
