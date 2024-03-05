"""国泰君安期货自定义绘图接口"""

import os
import io
import base64
import glob
import importlib
import matplotlib.pyplot as plt
from typing import Union, List
from .api import _get_global_var
from .base import Serie, Chart
from ._mychart.grammar import Sexp
from .util import http, urljoin


CHART_DICT = {}
for f in glob.glob(os.path.join(os.path.split(__file__)[0], "_mychart", "chart", "*")):
    _f = os.path.split(f)[-1]
    if _f.endswith(".py") or _f.endswith(".pyd") or _f.endswith(".so"):
        if not _f[0] in ('_', "."):
            k = _f.split(".")[0]
            module = importlib.import_module("grsh_data_api._mychart.chart.%s" % k)
            chart_class_name = "Chart" + "".join([v.capitalize() for v in k.split("_")])
            if not hasattr(module, chart_class_name):
                raise Exception(chart_class_name)
            chart_class = getattr(module, chart_class_name)
            assert chart_class.name == k

            gmpl_class_name = "Gmpl" + "".join([v.capitalize() for v in k.split("_")])
            if not hasattr(module, gmpl_class_name):
                raise Exception(gmpl_class_name)
            gmpl_class = getattr(module, gmpl_class_name)

            CHART_DICT[k.upper()] = dict(
                chart=chart_class,
                gmpl=gmpl_class,
                desc=chart_class.desc
            )


def chart_get_type_lst() -> List:
    """获取绘图类型的介绍

    Returns:
        list, 包含绘图类型和desc介绍
    """
    r = []
    for k in  sorted(CHART_DICT.keys()):
        r.append([k, CHART_DICT[k]['desc']])
    return r


def chart_with_grammar(grammar: str, param: dict = None) -> Chart:
    """根据自定义的语法绘图

    Args:
        grammar: 参考研究内容生成网站的图标中心
        param: dict，可配置的参数，目前支持参数 TODO

    Returns:
        base.Chart
    """

    # dict:
    #     - grammar
    #     - type_name
    #     - data_series: list of serie
    #     - info: list of info
    #     - param
    #     - var
    chart_data = Sexp(grammar).get_result()
    type_name = chart_data['type_name']

    if type_name not in CHART_DICT:
        raise Exception(f"{type_name} chart type error")

    _class = CHART_DICT[type_name]['chart']
    if param:
        for k, v in param.items():
            chart_data['param'][k] = v

    _obj = _class(**chart_data)
    return _obj


def chart_with_data(type_name: str, serie_lst: Union[List[Serie], Serie], param: dict = None) -> Chart:
    """使用数据绘图

    Args:
        type_name: str，绘图类型，参考chart_get_type_lst函数返回的字段
        serie_lst: list of Serie or Serie（grsh_data_api.base.Serie）, 使用api中的query可以直接获取Serie对象，
                   或者自己创建Serie对象
        param: dict, 可选参数 TODO

    Return:
        base.Chart

    """
    _class = CHART_DICT[type_name]['chart']

    # dict:
    #     - grammar
    #     - type_name
    #     - data_series: list of serie
    #     - param

    obj = _class(grammar='',
                 type_name=type_name,
                 serie_lst=serie_lst,
                 param=param,
                 )
    return obj


def chart_with_graphid(bussiness_id: str, param: dict=None) -> Chart:
    """通过图表中心的bussiness_id直接获得图表对象

    Args:
        graph_id: str, 图表中心的bussiness_id，可以通过auto.graph_query查询，也可直接查看网页
        param: dict，传递自定义的参数

    Returns:
        base.Chart
    """

    url = _get_global_var()['url']
    _url = urljoin(url, "/graphcenter2/query")
    rst = http(_url, post_data=dict(bussiness_id=bussiness_id), headers=_get_global_var()['headers'])
    grammar = rst['content']

    return chart_with_grammar(grammar, param)


def chart_save_current_plt_to_base64_str() -> str:
    """保存当前的plt对象至base64字符串，用户自定义图表的上传，参考auto.graph_upload_user_define

    Returns:
        str 图片的base64字符串
    """
    s = io.BytesIO()
    plt.tight_layout(pad=0.5)
    # plt.tight(pad=0.5)
    plt.savefig(s, format='png', dpi=300)
    return base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
