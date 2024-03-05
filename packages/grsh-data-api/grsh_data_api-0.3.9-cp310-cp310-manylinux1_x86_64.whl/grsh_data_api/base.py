"""绘图相关功能点中用到的类"""

import abc
import os
import pickle
import time
import pandas as pd
import matplotlib.pyplot as plt
from typing import Union, List, Dict
from threading import Lock
from ._mychart.util import chart_get_color_setting, get_mychart_app_config
from .util import Tool

LOCK = Lock()
MYCHART_APP_CONFIG = get_mychart_app_config()


class Serie:
    """绘图数据封装

    封装dataframe和info相关信息，提供加减乘除等运算支持。
    """
    def __init__(self,
                 df: pd.DataFrame,
                 gtjaqh_id: str,
                 name: str,
                 data_source: str = '国泰君安期货',
                 unit: str = None,
                 freq: str = None
                 ):
        """初始化

        Args:
            df: dataframe，columns必须为date value
            gtjaqh_id: str
            name: str
            data_source: str
            unit: str 可选
            freq: str 可选

        """

        assert list(df.columns) == ['date', 'value']
        df['value'] = df['value'].apply(lambda x: round(x, 8))

        self.df = df
        self.gtjaqh_id = gtjaqh_id
        self.name = name
        self.data_source = data_source
        self.unit = unit
        self.freq = freq

    def info_2_dict(self):
        return dict(
            gtjaqh_id=self.gtjaqh_id, name=self.name, unit=self.unit, freq=self.freq, data_source=self.data_source)

    @staticmethod
    def create_from_num(num, other):
        assert isinstance(other, Serie)
        df = other.df.copy()
        df['value'] = round(num, 8)
        return Serie(df, "", other.name, other.data_source, other.unit, other.freq)

    def get_info(self) -> dict:
        rst = {}
        for name in ["gtjaqh_id", "name", "data_source", "unit", "freq"]:
            if getattr(self, name) is not None:
                rst[name] = getattr(self, name)
        return rst

    def __add__(self, other):
        df1 = self.df.copy()
        df1 = df1.set_index('date')
        df2 = other.df.copy()
        df2 = df2.set_index('date')
        df = df1 + df2
        df = Tool.df_fill_to_end(df, "value")
        df = df.reset_index()
        df = df.dropna()
        return Serie(df, "", self.name, self.data_source, self.unit, self.freq)

    def __sub__(self, other):
        df1 = self.df.copy()
        df1 = df1.set_index('date')
        df2 = other.df.copy()
        df2 = df2.set_index('date')
        df = df1 - df2
        df = Tool.df_fill_to_end(df, "value")
        df = df.reset_index()
        df = df.dropna()
        return Serie(df, "", self.name, self.data_source, self.unit, self.freq)

    def __mul__(self, other):
        df1 = self.df.copy()
        df1 = df1.set_index('date')
        df2 = other.df.copy()
        df2 = df2.set_index('date')
        df = df1 * df2
        df = Tool.df_fill_to_end(df, "value")
        df = df.reset_index()
        df = df.dropna()
        return Serie(df, "", self.name, self.data_source, self.unit, self.freq)

    def __truediv__(self, other):
        df1 = self.df.copy()
        df1 = df1.set_index('date')
        df2 = other.df.copy()
        df2 = df2.set_index('date')
        df = df1 / df2
        df = Tool.df_fill_to_end(df, "value")
        df = df.reset_index()
        df = df.dropna()
        return Serie(df, "", self.name, self.data_source, self.unit, self.freq)

    def __repr__(self):
        return f"{self.gtjaqh_id}, {self.name}\n\n{self.df}\n\n"


class _Element:
    def __init__(self):
        self.data = None  # df, 绘图数据
        self.index = None  # list, x轴索引
        self.info = []  # list of dict, 数据字段信息
        self.data_source = set()  # set, 数据来源
        self.config = None  # dict, 配置
        self.chart_name = None  # str, 图表名称
        self.chart_num = None  # str, 图表数据长度
        self.chart_is_season = False  # bool, 是否是季节性
        self.chart_type = None  # str, 图表类型，bar的x轴需要特殊处理
        self.data_len = None  # int, 图表数据序列长度
        self.title = None  # str, 主标题
        self.subtitle = None  # str, 副标题
        self.chart_color = None  # 绘图颜色
        self.serie_lst = None  # 原始的serie对象列表

        # 额外的配置信息
        # title 自定义图表的标题
        # data_source: F关闭，其他的跳过自动部分，直接指定（国泰君安期货是默认都有）
        # legend_font_size_adjust 正负整数
        # legend_loc matplotlib中的图例位置参数：best
        self.param = None

    def generate_title(self):
        param = self.param
        if param and 'title' in param and param['title'] != 'T':
            self.title = param['title']
        else:
            need_title = ['table',
                          'line_season', 'line_season_area', 'line_season_week', 'line_lunar_season',
                          'template1_line_with_yoy', 'template4_bar_with_yoy']
            if (self.data_len == 1 and self.chart_num == '1') or self.chart_name in need_title:
                result = self.info[0]['name'].replace("：", ":")
                if 'unit' in self.info[0] and self.info[0]['unit']:
                    result += " (%s)" % self.info[0]['unit']
                self.title = result

    def generate_subtitle(self):
        if self.data_len == 1:
            self.subtitle = "%s=%s" % (
                self.index[-1],
                self.data.iloc[-1][self.data.columns[0]])

    def delay_cal(self):
        if self.data is not None:
            self.data_len = len(self.data.columns)
        else:
            self.data_len = 0
        self.generate_title()
        self.generate_subtitle()
        if self.data_len > 0:
            self.chart_color = chart_get_color_setting(self.config['color'], self.data_len, self.chart_is_season)
        # add data_source
        for info in self.info:
            if 'data_source' in info and info['data_source']:
                self.data_source.add(info['data_source'])


class Chart:
    """绘图类

    目前只支持mpl类型的绘图，通过prepare_data接口实现各种自定义的绘图数据处理，
    具体的绘图逻辑放在集成的子类的gmpl_class类属性中。

    """

    name = "_GChart"
    desc = None
    num = None
    chart_type = None
    is_season = False
    gmpl_class = None
    gechart_class = None

    def __init__(self, grammar: str, type_name: str, serie_lst: Union[List[Serie], Serie], param: Dict = None,
                 var: Dict = None):

        self._grammar = grammar

        # 将serie转换为lst
        if isinstance(serie_lst, Serie):
            serie_lst = [serie_lst,]

        self._data_series = serie_lst  # 原始数据

        # 返回前端的数据
        self.info = [v.get_info() for v in serie_lst]
        self.data = None  # prepare_data计算后的数据，和info一起返回给前端

        # 具体的绘制类对象
        self._gmpl = None
        self._gechart = None

        config = MYCHART_APP_CONFIG.copy()

        # print("\t",mpl.get_backend())

        self.element = _Element()
        self.element.config = config
        self.element.param = param
        self.element.chart_name = self.name
        self.element.chart_num = self.num
        self.element.chart_is_season = self.is_season
        self.element.chart_type = type_name
        self.element.serie_lst = serie_lst
        self.prepare_data()  # 初始化数据
        self.element.delay_cal()  # 延迟计算
        self.get_png()  # 直接用matplotlib绘图

    @abc.abstractmethod
    def prepare_data(self):
        pass

    def get_data_and_info(self):
        info = self.info
        _data = pd.DataFrame(self.data)
        if not self.is_season:
            _data = _data.reindex(index=_data.index[::-1])

        data = [list(item) for _, item in _data.iterrows()]

        '''
        _data= pd.DataFrame(self.data)
        print(_data)
        _columns = list(_data.columns)
        _data.columns = range(len(_columns))
        data = dict(columns = _columns, value = [dict(item) for _, item in _data.iterrows()])
        '''

        return dict(
            info=info,
            data=dict(columns=list(_data.columns), value=data)
        )

    def show(self):
        """使用plt.show()直接展示当前图片，注意mpl的egg设置"""
        plt.show()

    def get_png(self) -> str:
        """获取mpl绘图的base64字符串数据"""
        if self.gmpl_class:
            with LOCK:
                element_pickle_str = pickle.dumps(self.element)
                self._gmpl = self.gmpl_class(element_pickle_str)
                self._gmpl.plot()
                return self._gmpl.get_base64_png()

    def get_echart_option(self):
        if self.gechart_class:
            self._echart = self.gechart_class(self.element)
            self._echart.plot()
            return self._echart.get_echart_option()

    def save_png(self, filename: str=None) -> None:
        """直接保存mpl的绘图至文件

        Args:
            filename: str, 可选，默认为 ~/.myapp-data/tmp-时间戳.png

        """
        if filename is None:
            p = os.path.join(os.path.expanduser("~"), ".myapp-data")
            if not os.path.exists:
                os.mkdir(p)
            filename = os.path.join(p, f"tmp-{time.time()}.png")
        self._gmpl.save(filename)


