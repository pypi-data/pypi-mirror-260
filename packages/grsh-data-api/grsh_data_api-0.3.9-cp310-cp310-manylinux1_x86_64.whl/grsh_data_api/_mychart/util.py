import datetime
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict


def get_mychart_app_config() -> dict:
    def _load_config_color(filename):
        data = pd.read_excel(filename, engine='openpyxl', sheet_name=None)
        color_dict = {}
        for num, color_sheet in data.items():
            result = []
            for _, item in color_sheet.iterrows():
                result.append([item['r'] / 255.0, item['g'] / 255.0, item['b'] / 255.0])
            color_dict[f'color_{num}'] = result
        return color_dict

    # mpl setting
    # mpl.use('agg')
    # mpl.use('TkAgg')
    # if platform.platform().startswith("Windows"):
    #     mpl.use(_get_global_var()['mpl_backend'])
    # else:
    #     mpl.use('agg')
    # print(mpl.get_backend())
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['figure.figsize'] = (6, 4)
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['xtick.labelsize'] = 9
    plt.rcParams['ytick.labelsize'] = 9
    plt.rcParams.update({
        "figure.facecolor": (1.0, 1.0, 1.0, 0),
        "axes.facecolor": (1.0, 1.0, 1.0, 0),
        "savefig.facecolor": (1.0, 1.0, 1.0, 0),
    })

    config = dict()

    # chart setting
    config['left'] = 0.1
    config['right'] = 0.95
    config['bottom'] = 0.15
    config['top'] = 0.87
    config['font_size_title'] = 12
    config['font_size_subtitle'] = 10
    config['font_size_legend'] = 10
    config['font_size_datasource'] = 8
    config['font_size_note'] = 8

    # color setting
    filename_json = os.path.join(os.path.split(__file__)[0], "_config_color.json")
    filename_excel = os.path.join(os.path.split(__file__)[0], "_config_color.xlsx")
    if os.path.exists(filename_json):
        with open(filename_json, "r") as _f:
            config['color'] = json.load(_f)
    else:
        config['color'] = _load_config_color(filename_excel)

    # solar_lunar_mapping setting
    solar_lunar_mapping = pd.read_csv(os.path.join(os.path.split(__file__)[0], "_solar_lunar_mapping.csv"))
    solar_lunar_mapping['solar_date'] = pd.to_datetime(solar_lunar_mapping['solar_date']).apply(lambda x: x.date())
    config['solar_lunar_mapping'] = solar_lunar_mapping

    return config



def chart_get_color_setting(color, num: int, season: bool = False):
    if num <= 9:
        color = color[f'color_{num}']
    else:
        color = color['color_9']
        init_color = color.copy()
        for i in range(10, num + 1):
            color.append(init_color[i % 9 - 1] + [3 / (i - 6)])
    if season:
        color = [[1, 0, 0]] + color
        color = color[:num]
    return color


def strategy_xtick_label_cut(xtick: List, info: Dict):
    # todo 优化下算法
    if len(xtick) >= 8 and len(xtick) <= 12:
        skip = 2
        loc = sorted(list(range(len(xtick) - 1, 0, -skip)))
    elif len(xtick) > 12:
        n = 6
        total = len(xtick) - 1
        tmp = total % n
        skip = int((total - tmp) / n)
        if tmp > skip:
            tmp = tmp - int(tmp / skip) * skip
        loc = list(range(tmp, total + 1, skip))

    # unit = int(len(xtick) / n)
    # loc = list(range(unit, len(xtick), unit))
    label = [xtick[v] for v in loc]

    if isinstance(xtick[0], datetime.date) and isinstance(label[0], datetime.date) and \
            info is not None and 'freq' in info:  # and isinstance(self._index, dict):
        if info['freq'] == '年':
            label = [v.year for v in label]
        if info['freq'] == '月':
            label = [format(v, "%Y/%m") for v in label]
        else:
            pass
            # try:
            #    label = [format(v, '%Y%m%d') for v in label]
            # except:
            #    pass

    return loc, label


def strategy_xtick_label_year(xtick: List):
    loc = []
    label = []
    for i in range(1, len(xtick)):
        item_pre = xtick[i - 1]
        item = xtick[i]

        if item.year != item_pre.year:
            loc.append(i)
            label.append(item.year)
    year_gap = len(loc) // 20 + 1
    loc = [value for index, value in enumerate(loc) if index % year_gap == 0]
    label = [value for index, value in enumerate(label) if index % year_gap == 0]

    return loc, label
