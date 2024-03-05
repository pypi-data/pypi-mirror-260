"""国泰君安期货研究所API接口，提供指标数据库、行情数据、绘图和仪表盘自动化等相关功能

使用案例:

.. code-block:: python
   :linenos:

   menu = get_edb_menu()
   df1 = get_edb_data("ID001260", "20100101", "20210101")
   df2 = get_edb_data_detail("ID001260", "20100101", "20210101")
"""


import time
import json
import hashlib
import requests
import pandas as pd
from . import LOGO
from .base import Serie
from .util import urljoin
from ._service.edb import ServiceEdbHttp, ParamGtjaqhid, ParamEdbdata


_IS_INITED = False
_HEADERS = {}
_LOGIN_TIME = None
_URL = None
_USER_NAME = None


def _get_global_var():
    if _LOGIN_TIME is None:
        raise Exception("please login first")

    return dict(
        headers=_HEADERS,
        login_time=_LOGIN_TIME,
        url=_URL,
        user_name=_USER_NAME,
    )


def INIT(user: str, password: str, url: str, is_hashed: bool = False):
    """初始化接口

    Args:
        user: 用户名
        password: 密码，如果传递md5后的字符串，需要设置is_hashed=True
        url: Http地址
        is_hashed: 见password，默认为False

    Usage:
      >>> INIT(username, password, url, is_hashed=True)

    """

    global _IS_INITED
    global _HEADERS
    global _URL
    global _LOGIN_TIME
    if not _IS_INITED or time.time() - _LOGIN_TIME >= 14000-100:
        if not is_hashed:
            md5 = hashlib.md5(password.encode("utf-8"))
            password = md5.hexdigest()
        req = requests.post(urljoin(url, "/login_jwt/login"), dict(user=user, password=password))
        data = json.loads(req.text)
        if 'access_token' not in data['data']:
            raise Exception("init failed, please check user and password")
        else:
            _HEADERS = {'Authorization': 'Bearer %s' % data['data']['access_token']}
            _URL = url
            _IS_INITED = True
            _USER_NAME = user
            _LOGIN_TIME = time.time()
            print(LOGO)
    else:
        print(LOGO)


def get_edb_menu() -> pd.DataFrame:
    """获取国泰君安期货产业数据所有目录

    Returns:
        返回pd.DataFrame，字段包括：gtjaqh_id, name, unit, freq, data_source, original_data_source
    """
    url = _get_global_var()['url']
    headers = _get_global_var()['headers']
    obj = ServiceEdbHttp(url, headers)
    return obj.get_edb_menu()


def get_edb_data(gtjaqh_id: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
    """获取edb指标时间序列

    Args:
        gtjaqh_id: 自定义的id，格式为DI+6位数字
        start_date: 可选参数，序列开始时间yyyymmdd格式
        end_date: 可选参数，序列结束时间yyyymmdd格式

    Returns:
        pd.DataFrame，包括date,value字段
    """
    url = _get_global_var()['url']
    headers = _get_global_var()['headers']
    obj = ServiceEdbHttp(url, headers)
    return obj.get_data(ParamEdbdata(**dict(gtjaqh_id=gtjaqh_id, start_date=start_date, end_date=end_date)))


def get_edb_data_detail(gtjaqh_id: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
    """获取edb指标时间序列，在get_edb_data的基础上返回历史版本和历史版本创建的时间戳

    Args:
        gtjaqh_id: 自定义的id，格式为DI+6位数字
        start_date: 可选参数，序列开始时间yyyymmdd格式
        end_date: 可选参数，序列结束时间yyyymmdd格式

    Returns:
        pd.DataFrame，包括date,value,serial,create_dt
    """
    url = _get_global_var()['url']
    headers = _get_global_var()['headers']
    obj = ServiceEdbHttp(url, headers)
    return obj.get_data_detail(ParamEdbdata(gtjaqh_id=gtjaqh_id, start_date=start_date, end_date=end_date))


def get_edb_info(gtjaqh_id: str) -> dict:
    """获取edb指标数据的info信息

    Args:
        gtjaqh_id (str): 自定义的id，格式为DI+6位数字

    Returns:
        dict
    """
    url = _get_global_var()['url']
    headers = _get_global_var()['headers']
    obj = ServiceEdbHttp(url, headers)
    return obj.get_info(ParamGtjaqhid(gtjaqh_id=gtjaqh_id))


def query(gtjaqh_id: str, start_date: str = None, end_date: str = None, option: dict=dict()) -> Serie:
    """查询指标，返回Serie，用于绘图函数

    Args:
        gtjaqh_id: 自定义的id，格式为DI+6位数字
        start_date: 可选参数，序列开始时间yyyymmdd格式
        end_date: 可选参数，序列结束时间yyyymmdd格式

    Returns:
        Serie

    """
    url = _get_global_var()['url']
    headers = _get_global_var()['headers']
    obj = ServiceEdbHttp(url, headers)

    p1 = ParamEdbdata(gtjaqh_id=gtjaqh_id, start_date=start_date, end_date=end_date)
    p2 = ParamGtjaqhid(gtjaqh_id=gtjaqh_id)

    df = obj.get_data(p1)
    info = obj.get_info(p2)

    s = Serie(df, **info)
    if 'name' in option:
        s.name = option['name']
    if 'unit' in option:
        s.unit = option['unit']
    return s


def get_quo_data(contract, fields, start_date: str = None, end_date: str = None):
    """获取期货日行情数据，提供二次加工合约

    Args:
        contract: 合约代码，具体合约按照 "code（小写）+yymm" 格式；
                  支持二次加工合约，如：cu_index（合约加权指数），cu_active（连续合约）
        fields: 导出字段，逗号分割字符串: contract_real,exchange,code,preclose,open,high,low,close,settle,vol,oi,amount
        start_date: 可选，开始日期，yyyymmdd
        end_date: 可选，结束日期，yyyymmdd

    Returns:
        pd.DataFrame
    """
    post_data = dict(contract=contract, fields=fields, start_date=start_date, end_date=end_date)
    url = urljoin(_get_global_var()['url'], "dataapi/quo")
    rst = requests.post(url, json=post_data, headers=_get_global_var()['headers'])
    if rst.status_code == 200:
        rst = json.loads(rst.text)
        if 'code' in rst and rst['code'] == 0:
            rst = pd.DataFrame(rst['data'])
            for v in ['preclose', 'open', 'high', 'low', 'close', 'oi', 'vol', 'settle', 'amount']:
                if v in rst.columns:
                    rst[v] = rst[v].apply(lambda x: float(x) if x != '' else None)
            # rst['value'] = rst['value'].apply(lambda x: float(x))
            return rst
        else:
            raise Exception(rst['msg'])
    else:
        raise Exception(f"http status code {rst.status_code}")
