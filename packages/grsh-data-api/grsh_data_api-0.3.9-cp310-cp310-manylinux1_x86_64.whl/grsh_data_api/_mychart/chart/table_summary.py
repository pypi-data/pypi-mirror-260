import pandas as pd
from dateutil.relativedelta import relativedelta
from grsh_data_api._mychart.base import GMPL, plt, mpl
from grsh_data_api._mychart.chart.line_multi import ChartLineMulti


class GmplTableSummary(GMPL):
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
        param = self.element.config['param']
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
        tab = plt.table(
            cellText=self.element.data.values.tolist(),
            colLabels=self.element.data.columns,
            rowLabels=self.element.index,
            loc='center',
            cellLoc='center',
            rowLoc='center')
        tab.auto_set_font_size(False)
        tab.set_fontsize(10)
        # col_max_length = list(self.element.data.apply(lambda x: len(str(x))))
        # print(col_max_length)
        tab.auto_set_column_width(self.element.data.columns)
        # tab.auto_set_column_width(col=list(range(len(self.element.data.columns))))
        tab.scale(1, 2)
        plt.suptitle(self.element.title, y=0.9)
        plt.axis('off')

        self._current_ax1 = ax

    def plot(self):
        try:
            self._plot()
            self._set_general()
            # self._set_title()
            self._save_base64()
        except Exception as e:
            raise e
        finally:
            plt.close("all")


class ChartTableSummary(ChartLineMulti):
    name = "table_summary"
    desc = "多数据表格"
    num = "N"
    gmpl_class = GmplTableSummary

    def prepare_data(self):

        def _get_item_by_date(_df, _date):
            if _df['date'].max() >= _date:
                return _df[_df['date'] <= _date].iloc[-1]['value']
            else:
                return None

        result = []
        for i, item in enumerate(self._data_series):
            data = item.df
            info = item.get_info()
            self.element.info.append(info)
            data['date'] = pd.to_datetime(data['date'])
            data['date'] = data['date'].apply(lambda x: x.date())

            data = data.sort_values("date")

            date_latest = data['date'].max()
            date_pre_week = date_latest - relativedelta(weeks=1)
            date_pre_month = date_latest - relativedelta(months=1)
            date_pre_year = date_latest - relativedelta(years=1)

            d1 = _get_item_by_date(data, date_latest)
            d2 = _get_item_by_date(data, date_pre_week)
            d3 = _get_item_by_date(data, date_pre_month)
            d4 = _get_item_by_date(data, date_pre_year)

            # d5 = len(data[data['value'] <= d1]) / len(data) * 100

            _result = {
                "name": info['name'],
                "最新值": "%.1f" % d1,
                "周同比": "%.f%%" % ((d1 / d2 - 1) * 100) if d2 is not None else "-",
                "月同比": "%.1f%%" % ((d1 / d3 - 1) * 100) if d3 is not None else "-",
                "年同比": "%.f%%" % ((d1 / d4 - 1) * 100) if d4 is not None else "-",
                # "分位数估计": "%.1f%% (%s起)" % (d5, format(data['date'].min(), "%Y%m"))
            }
            result.append(_result)

        data = pd.DataFrame(result)
        print(data)
        data = data.set_index("name")

        self.element.index = list(data.index)
        self.element.data = data
