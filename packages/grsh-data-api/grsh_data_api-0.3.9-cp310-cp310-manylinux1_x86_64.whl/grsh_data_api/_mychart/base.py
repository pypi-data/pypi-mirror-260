import io
import re
import abc
import copy
import pickle
import base64
import datetime
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from threading import Lock
from loguru import logger
from . import get_mpl_backend
from .util import get_mychart_app_config
from .util import strategy_xtick_label_cut, strategy_xtick_label_year, chart_get_color_setting
from ..base import Chart

MYCHART_APP_CONFIG = get_mychart_app_config()
GMPL_DEFAULT_FIGURE_SIZE = (6, 4)


class GMPL:
    def __init__(self, element_pick_str: bytes):

        _agg = get_mpl_backend()
        if _agg and _agg == 'agg':
            mpl.use("agg")

        element = pickle.loads(element_pick_str)
        # 初始mpl
        # mpl.use('agg')
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['figure.figsize'] = GMPL_DEFAULT_FIGURE_SIZE
        plt.rcParams['savefig.dpi'] = 200
        plt.rcParams['xtick.labelsize'] = 9
        plt.rcParams['ytick.labelsize'] = 9
        plt.rcParams.update({
            "figure.facecolor": (1.0, 1.0, 1.0, 0),
            "axes.facecolor": (1.0, 1.0, 1.0, 0),
            "savefig.facecolor": (1.0, 1.0, 1.0, 0),
        })

        self.element = element
        if self.element.data_len > 0:
            self.chart_color = chart_get_color_setting(
                element.config['color'],
                element.data_len,
                element.chart_is_season)
        self.byte_png = None
        self.base64_png = None
        self._current_ax1 = None
        self._current_ax2 = None
        self._lock = Lock()

        if self.element.param:
            param = self.element.param
            width, height = GMPL_DEFAULT_FIGURE_SIZE
            if 'width' in param:
                width = 6 * float(param['width'])
            if 'height' in param:
                height = 4 * float(param['height'])
            logger.debug(f"reset fig size with ({width}, {height})")
            plt.rcParams['figure.figsize'] = (width, height)

            # plt.figure(figsize=(width, height))

    def _set_datasource(self, ax:mpl.axes.Axes):
        # set data source
        param = self.element.param

        label_data_source = "资料来源: 国泰君安期货研究"
        if param is None:
            for v in self.element.data_source:
                if v not in ('GTJAQH', '国泰君安期货'):
                    label_data_source += ", %s" % v
        else:
            if 'data_source' not in param or ('data_source' in param and param['data_source'] != 'F'):
                for v in self.element.data_source:
                    if v not in ('GTJAQH', '国泰君安期货'):
                        label_data_source += ", %s" % v
            else:
                label_data_source += f", {param['data_source']}"

        if not (param and ('data_source' in param and param['data_source'] == 'F')):
            ax.text(1.03, -0.15, label_data_source,
                    multialignment='center',
                    verticalalignment='bottom',
                    horizontalalignment='right',
                    fontsize=self.element.config['font_size_datasource'],
                    transform=ax.transAxes)

    def _set_general(self, ax: mpl.axes.Axes = None):
        if not ax:
            ax = self._current_ax1

        config = self.element.config
        plt.subplots_adjust(
            left=config['left'],
            right=config['right'],
            top=config['top'],
            bottom=config['bottom'],
        )
        ax.set_xlabel(None)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        param = self.element.param
        if param and 'x_pos' in param:
            loc = int(param['x_pos'])
            ax.spines['bottom'].set_position(('data', loc))

        self._set_datasource(ax)

    def _set_title(self, ax: mpl.axes.Axes = None, y: float = 1.05):
        if not ax:
            ax = self._current_ax1
        if self.element.title:
            plt.title(
                y=y,
                label=self.element.title,
                fontsize=self.element.config['font_size_title'],
                transform=ax.transAxes
            )

    def _set_subtitle(self, ax: mpl.axes.Axes = None):
        if not ax:
            ax = self._current_ax1
        if self.element.subtitle:
            ax.text(0.5,
                    self.element.config['top'] + 0.12,
                    self.element.subtitle,
                    horizontalalignment='center',
                    multialignment='left',
                    verticalalignment='bottom',
                    fontsize=self.element.config['font_size_note'],
                    transform=ax.transAxes)

    def _set_legend_position(self, ax: mpl.axes.Axes = None):
        # 设置图例
        if not ax:
            ax = self._current_ax1

        if self.element.chart_is_season:
            loc = "best"
            font_size = self.element.config['font_size_legend'] - 2
        else:
            loc = "upper center"
            if self.element.data_len >= 6:
                font_size = self.element.config['font_size_legend'] - 2
            else:
                font_size = self.element.config['font_size_legend']

        if self.element.param and 'legend_loc' in self.element.param:
            loc = self.element.param['legend_loc']

        if self.element.param and 'legend_font_size_adjust' in self.element.param:
            try:
                _tmp = int(self.element.param['legend_font_size_adjust'])
                font_size = max(self.element.config['font_size_legend'] + _tmp, 6)
            except:
                pass

        if self.element.title is None and self.element.subtitle is None:
            # 如果不存在title
            legend_len_max = max([len(i) for i in self.element.data.columns])
            legend_avg = int(np.mean([len(i) for i in self.element.data.columns]))
            if legend_len_max > 37 and legend_avg > 15:
                ax.legend(loc=loc,
                          ncol=1,
                          frameon=False,
                          bbox_to_anchor=(0.5, 1.12) if loc == "upper center" else None,
                          fontsize=font_size)
            else:
                ax.legend(loc=loc,
                          ncol=2,
                          frameon=False,
                          bbox_to_anchor=(0.5, 1.12) if loc == "upper center" else None,
                          fontsize=font_size)
        else:
            # 存在title, subtitle不应该和legend并存
            ax.legend(loc=loc,
                      frameon=False,
                      bbox_to_anchor=(0.5, 1.05) if loc == "upper center" else None,
                      fontsize=font_size
                      )

    def _set_xtick(self, ax: mpl.axes.Axes = None, rotation: int = None):
        # 设置x轴坐标

        if not ax:
            ax = self._current_ax1

        # bar 设置
        if self.element.chart_type.startswith('BAR'):
            rotation = 360
            ax.set_xlim([-0.5, len(self.element.data)])
        else:
            ax.set_xlim([self.element.data.index[0], self.element.data.index[-1]])

        # 标签
        if len(self.element.index) < 10:
            loc = range(len(self.element.index))
            label = list(self.element.index)
        elif self.element.index[-1].year - self.element.index[0].year > 3 and \
                pd.Series(self.element.index).diff().mean().days < 300:
            loc, label = strategy_xtick_label_year(self.element.index)
        else:
            loc, label = strategy_xtick_label_cut(self.element.index, self.element.info[0])

        ax.set_xticks(loc)
        if rotation:
            ax.set_xticklabels(label, rotation=rotation)
        else:
            ax.set_xticklabels(label)

    def _set_hline_area(self, ax: mpl.axes.Axes = None, ymin=0, ymax=0.98):
        def _is_number(x):
            try:
                float(x)
                return True
            except (ValueError, TypeError):
                pass

        def _hline_single(x1, x2, color):
            _, xlim = ax.get_xlim()
            if isinstance(self.element.index[0], datetime.date):
                x1 = pd.to_datetime(x1).date()
                x2 = pd.to_datetime(x2).date()
            if isinstance(self.element.index[0], datetime.date) or re.match("^[0-9]{2}-[0-9]{2}$",
                                                                            self.element.index[0]):
                x1_loc = [index + 1 for index, value in enumerate(self.element.index) if x1 >= value]
                x2_loc = [index + 1 for index, value in enumerate(self.element.index) if x2 >= value]
                xmin = x1_loc[-1] / len(self.element.index) * xlim
                xmax = x2_loc[-1] / len(self.element.index) * xlim
                ax.axvspan(xmin, xmax, ymin, ymax, alpha=0.2, color=color)
            if _is_number(x1) and _is_number(x2):
                x1 = float(x1)
                x2 = float(x2)
                ax.axvspan(x1 * xlim, x2 * xlim, ymin, ymax, alpha=0.2, color=color)

        param = self.element.param
        if param and 'hline' in param:
            loc = param['hline']
            if not ax:
                ax = self._current_ax1

            hline_color = np.array([[31, 119, 180], [51, 102, 255], [255, 116, 97], [255, 185, 66]]) / 255
            hline_color = hline_color.tolist()
            loc_lst = loc.replace(" ", "").split(';')
            hline_color = hline_color * len(loc_lst)

            for num, i in enumerate(loc_lst):
                try:
                    s, e = i.split(',')
                except ValueError:
                    raise Exception("hline input must be a pair")
                try:
                    _hline_single(s, e, hline_color[num])
                except Exception as e:
                    raise Exception("invalid hline input %s" % e)

    def _set_background(self, ax: mpl.axes.Axes=None):
        if not ax:
            ax = self._current_ax1
        config = self.element.config
        param = self.element.param
        if param and "background" in param:
            ax.text(0.5, 0.5, '国 泰 君 安 期 货',
                    transform=ax.transAxes,
                    fontsize=50, color='gray',
                    alpha=0.1,
                    ha='center',
                    va='center',
                    rotation=30
                    )

    def _save_base64(self):
        s = io.BytesIO()
        plt.tight_layout(pad=0.5)
        plt.savefig(s, format='png', dpi=300)
        self.byte_png = copy.copy(s)
        s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
        self.base64_png = s

    @abc.abstractmethod
    def _plot(self):
        pass

    def plot(self):
        try:
            with self._lock:
                param = self.element.param
                plt.close('all')
                self._plot()
                self._set_general()
                self._set_title()
                # self._set_subtitle()    # todo 存在bug，无限期弃用
                self._set_legend_position()
                if not (param and 'skip_set_xtick' in param):
                    self._set_xtick()
                self._set_hline_area()
                self._set_background()
                self._save_base64()
        except Exception as e:
            raise e
        finally:
            pass
            # plt.cla()
            # plt.clf()
            # plt.close('all')

    def save(self, filename: str):
        with open(filename, "wb") as f:
            f.write(self.byte_png.getvalue())

    def get_base64_png(self):
        return self.base64_png


class GECHART:
    def __init__(self, element: object):
        self.element = element
        self.option = dict(
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
        self.template = None

    @abc.abstractmethod
    def plot(self):
        pass

    def save(self, filename: str=None):
        with open(filename, "w", encoding='utf-8') as f:
            f.write(self.template)

    def get_echart_option(self):
        return self.option

    def _config_color(self, i):
        item = self.element.chart_color[i].copy()
        if len(item) == 3:
            item.append(1)
        return "rgba(%s,%s,%s,%s)" % (item[0] * 255, item[1] * 255, item[2] * 255, item[3])
