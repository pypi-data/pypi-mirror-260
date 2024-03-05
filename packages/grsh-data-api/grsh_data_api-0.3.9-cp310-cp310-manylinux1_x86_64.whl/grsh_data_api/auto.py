"""提供api接口操作研究生成平台的图表中心和仪表盘

注意: 图表中心和仪表盘使用：类型（个人、公用），用户，path，name作为唯一逐渐，目前的api接口默认在"个人、用户"先增删改查数据条目

.. code-block:: python
   :linenos:

   # 上传图表demo1
   # 一些自定义的plt代码 。。。
   from grsh_data_api.chart import chart_save_current_plt_to_base64_str
   data = chart_save_current_plt_to_base64_str()
   graph_upload_user_define(path="/demo/123", name="demo")    # 将自定以的图表上传到图表中心，注意；未来的更新也需要当前用户更新

   # 上传图表demo2，批量创建指数走势
   for v in ['rb', 'cu', 'c', 'cs']:
       graph_create(
           path="/demo/888",
           name=f"{v}指数走势",
           content=f"(LINE_SINGLE (SERIE {v}_index:close)")

   # 查询和批量删除
   for item in graph_query(path='/demo/888'):
       graph_delete(item['bussiness_id'])
"""

import uuid
import json
from typing import List, Dict
from grsh_data_api import _get_global_var
from grsh_data_api.util import urljoin, http


def graph_create(path: str, name: str, content: str):
    """图表中心创建

    Args:
        path: str
        name: str
        content, str 自定义的绘图语法

    Returns:
        str, 返回图表id（int）
    """
    url = _get_global_var()['url']
    headers = _get_global_var()['headers']

    rst = http(urljoin(url, '/graphcenter2/create'),
               post_data=dict(kind='person', path=path, name=name, content=content),
               headers=headers)
    return rst


def graph_query(path: str, name: str = None) -> list:
    """图表中心查询

    Args:
        path: str
        name: str 可选

    Returns:
        list
    """
    url = _get_global_var()['url']
    headers = _get_global_var()['headers']

    post_data = dict(path=path)
    if name:
        post_data['name'] = name

    rst = http(urljoin(url, '/graphcenter2/query'),
               post_data=post_data,
               headers=headers)
    return rst


def graph_delete(bussiness_id: str) -> str:
    """图表中心删除

    Args:
        bussiness_id: str, uuid

    Returns:
        str
    """
    url = _get_global_var()['url']
    headers = _get_global_var()['headers']
    rst = http(urljoin(url, '/graphcenter2/delete'),
               post_data=dict(bussiness_id=bussiness_id),
               headers=headers)
    return rst


def graph_upload_user_define(path: str, name: str, base64_str: str) -> str:
    """图表中心上传自定义的绘图

    Args:
        path: str
        name: str
        base64_str: str

    Returns:
        str
    """
    url = urljoin(_get_global_var()['url'], "/graphcenter2/uploaduserdefine")
    rst = http(url, post_data=dict(path=path, name=name, base64_str=base64_str), headers=_get_global_var()['headers'])
    return rst


class DashboardElement:
    pass


class DashboardG7Title5(DashboardElement):
    """仪表盘中的文字组件，格式同word模板中的G7Title5"""

    def __init__(self, title: str):
        """创建G7Title5

        Args:
            title: str

        """
        self.value = dict(
            id=str(uuid.uuid4()),
            name="G7Title5",
            propsData={
                'content': title
            },
            left=0,
            top=0,
            width=500,
            height=30,
        )


class DashboardImg1(DashboardElement):
    """仪表盘中的图片组件

    支持两种格式的图片，1直接传递图表中心的bussiness_id（因为无论是type是在个人还是在公共，都支持，注意使用graph_upload_user_define
    上传的图片需要图片上传人运维。2直接传递grammar，跳过图表中心创建图表，直接在仪表盘中使用grammar，后端渲染获得图片。

    Args:
        title: str
        bussiness_id: str, 可选
        grammar: str，可选，grammar存在的时候优选使用grammar
    """

    def __init__(self, title: str, bussiness_id: str = None, grammar: str = None):
        """创建仪表盘中图片组件

        Args:
            title: str
            bussiness_id: str 图表中心的bussiness_id
            grammar: str 自定义绘图语法
        """
        props_data = dict(title=title)
        if grammar:
            props_data['gramContent'] = grammar
        else:
            if bussiness_id:
                props_data['bussinessId'] = bussiness_id
            else:
                raise Exception("must provide grammar or bussiness_id")

        self.value = {
            "id": str(uuid.uuid4()),
            "name": "Img1",
            "propsData": props_data,
            "left": 0,
            "top": 0,
            "width": 500,
            "height": 340,
        }


def dashboard_create(path: str, name: str, element_lst: List) -> str:
    """仪表盘创建，默认使用行模式自动布局

    Args:
        path: str
        name: str
        element_lst: list of list of DashboardElement

    Returns:
        str
    """

    WIDTH = 500
    HEIGHT = 340

    def _modify_item_size(item):
        item['height'] = round(item['height'], -1)
        item['width'] = round(item['width'], -1)
        return item

    def _add_param(result):
        for item in result:
            if item['name'] == 'Img1':
                _param = dict(background='T')
                _param['height'] = item['height'] / HEIGHT
                _param['width'] = item['width'] / WIDTH
                item['param'] = _param
        return result

    # 行模式智能布局：1. 确定层次； 2. 同一层从左向右排序
    result = []
    start_top = 0
    next_top = 0
    for level in element_lst:
        # level = sorted(level, key=lambda x: x['left'])
        for i in range(len(level)):
            item = level[i].value
            if i == 0:
                item['top'] = start_top
                item['left'] = 0
            else:
                pre_item = level[i - 1].value
                item['top'] = start_top
                item['left'] = pre_item['left'] + pre_item['width']
            result.append(item)
            next_top = max(next_top, start_top + item['height'])
        start_top = next_top

    content = _add_param(result)

    url = _get_global_var()['url']
    headers = _get_global_var()['headers']
    rst = http(url + '/officetemplate/add',
               post_data=dict(
                   kind='person',
                   type='png',
                   path=path,
                   name=name,
                   content=json.dumps(content)),
               headers=headers)
    return rst


def dashboard_query(path: str = None, name: str = None) -> List:
    """仪表盘查询

    如果不传递path和name参数，默认返回所用户个人下的所有仪表盘。

    Args:
        path: str
        name: str

    Returns:
        list
    """

    url = _get_global_var()['url']
    headers = _get_global_var()['headers']

    post_data = dict(path=path)
    if name:
        post_data['name'] = name

    rst = http(url + '/officetemplate/query',
               post_data=post_data,
               headers=headers)
    return rst


def dashboard_delete(bussiness_id: str):
    """仪表盘删除

    Args:
        bussiness_id: str

    Returns:
        str
    """

    url = _get_global_var()['url']
    headers = _get_global_var()['headers']
    return http(urljoin(url, '/officetemplate/delete2'),
                post_data=dict(bussiness_id=bussiness_id),
                headers=headers)
