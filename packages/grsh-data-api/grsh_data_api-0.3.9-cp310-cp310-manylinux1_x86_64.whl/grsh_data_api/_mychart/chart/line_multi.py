import json
import pandas as pd
from grsh_data_api.util import Tool
from grsh_data_api._mychart.base import Chart, GMPL, GECHART, mpl, plt


class GmplLineMulti(GMPL):
    def _plot(self):
        self._current_ax1 = self.element.data.plot(color=self.chart_color)


'''
class GechartLineMulti(GECHART):
    def plot(self):
        # title = self.get_title_text()
        xaxis = [str(v) for v in self.element.index]

        # s = [list(self.element.data[self.element.data.columns[i]]) for i in range(len(self.element.data.columns))]
        s = []
        for i, name in enumerate(self.element.data.columns):
            _t = self.element.data[name].copy()
            _t = _t.fillna('')
            # s.append(dict(serie=list(_t), name=str(self.element.info[i]['name']), color=self._config_color(i)))
            s.append(
                dict(type='line', data=list(_t), name=str(self.element.info[i]['name']), color=self._config_color(i)))

        option = dict(
            xAxis=dict(data=xaxis),
            series=s,

            legend={},

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
        self.template = CHART_TEMPLATE.substitute(OPTION_JSON=option_json)
'''


class ChartLineMulti(Chart):
    name = "line_multi"
    desc = "多折现图"
    num = "N"
    gmpl_class = GmplLineMulti
    def prepare_data(self):
        result = []
        for i, item in enumerate(self._data_series):
            data = item.df
            info = item.get_info()
            self.element.info.append(info)

            data['date'] = pd.to_datetime(data['date'])
            data['date'] = data['date'].apply(lambda x: x.date())
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
