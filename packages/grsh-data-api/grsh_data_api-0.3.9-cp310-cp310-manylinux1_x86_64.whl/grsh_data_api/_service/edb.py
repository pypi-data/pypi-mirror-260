import re
import datetime
import pandas as pd
from typing import Optional
from dateutil.parser import parse
from pydantic import BaseModel, validator  # pydantic 1.xxx
from grsh_data_api.util import urljoin


# model ----------------------------------------------------------------------------------------------------------------
def validator_gtjaqh_id(v):
    # 单指标校验，支持IDxxxxxx和行情contract:field两种结构
    v = v.strip().replace("：", ":").replace('，', ',').replace(' ', '')
    if len(v.split(",")) > 1:
        raise Exception(f"not support gtjaqh_id {v}")

    tmp = v.split(":")
    if len(tmp) == 2:
        # quo
        contract, field = tmp
        if field not in ['close', 'open', 'high', 'low', 'settle', 'presettle', 'preclose', 'vol', 'oi', 'amount']:
            raise Exception(f"quo not supprt field {field}")
        return v
    else:
        pat = re.compile("^ID[0-9]{6}$")
        if pat.match(v):
            return v
        else:
            raise Exception(f"not support gtjaqhid {v}")


def validator_date(v):
    if v:
        return parse(str(v)).date()
    else:
        return v


class ParamGtjaqhid(BaseModel):
    gtjaqh_id: str

    @validator("gtjaqh_id", pre=True, always=True)
    def set_gtjaqh_id(cls, v):
        return validator_gtjaqh_id(v)


class ParamEdbdata(BaseModel):
    gtjaqh_id: str
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None

    @validator("gtjaqh_id", pre=True, always=True)
    def set_gtjaqh_id(cls, v):
        return validator_gtjaqh_id(v)

    @validator("start_date", pre=True, always=True)
    def set_start_date(cls, v):
        return validator_date(v)

    @validator("end_date", pre=True, always=True)
    def set_end_date(cls, v):
        return validator_date(v)


# repo -----------------------------------------------------------------------------------------------------------------
def _se_condition(start_date: datetime.date, end_date: datetime.date) -> str:
    condition = ""
    if start_date:
        condition += " and date>='%s' " % start_date
    if end_date:
        condition += " and date<='%s' " % end_date
    return condition


class RepoEdb:
    def get_data(self, param: ParamEdbdata) -> pd.DataFrame:
        raise Exception()

    def get_data_detail(self, param: ParamEdbdata) -> pd.DataFrame:
        raise Exception()

    def get_info(self, param: ParamGtjaqhid) -> dict:
        raise Exception()


class RepoEdbMysql(RepoEdb):
    def __init__(self, database):
        self._database = database

    def _find_gtjaqhid_db_tb_info(self, gtjaqh_id: str):
        with self._database.with_conn() as conn:
            sql1 = "select data_dbname,data_tbname from edb_info where gtjaqh_id=%(gtjaqh_id)s;"
            data1 = self._database.safe_read_sql(sql1, dict(gtjaqh_id=gtjaqh_id), conn)
            if len(data1) != 1:
                raise Exception(f"can not find gtjaqhid={gtjaqh_id}")
            dbname = data1.iloc[0]['data_dbname']
            tbname = data1.iloc[0]['data_tbname']
            return dbname, tbname

    def get_data(self, param: ParamEdbdata) -> pd.DataFrame:
        with self._database.with_conn() as conn:
            dbname, tbname = self._find_gtjaqhid_db_tb_info(param.gtjaqh_id)
            condition = _se_condition(param.start_date, param.end_date)
            sql = f"select date, value from {dbname}.{tbname} " \
                  f"where gtjaqh_id=%(gtjaqh_id)s and serial=0 {condition} order by date;"
            data = self._database.safe_read_sql(sql, dict(gtjaqh_id=param.gtjaqh_id), conn)
            data['value'] = data['value'].apply(lambda x: float(x))
            return data

    def get_data_detail(self, param: ParamEdbdata) -> pd.DataFrame:
        with self._database.with_conn() as conn:
            dbname, tbname = self._find_gtjaqhid_db_tb_info(param.gtjaqh_id)
            condition = _se_condition(param.start_date, param.end_date)
            sql = f"select date, value, serial, create_dt from {dbname}.{tbname} " \
                  f"where gtjaqh_id=%(gtjaqh_id)s and serial=0 {condition} order by date desc;"
            data = self._database.safe_read_sql(sql, dict(gtjaqh_id=param.gtjaqh_id), conn)
            data['value'] = data['value'].apply(lambda x: float(x))
            return data

    def get_info(self, param: ParamGtjaqhid) -> dict:
        with self._database.with_conn() as conn:
            sql = "select gtjaqh_id, name, unit, freq, data_source from edb_info where gtjaqh_id=%(gtjaqh_id)s;"
            df = self._database.safe_read_sql(sql, dict(gtjaqh_id=param.gtjaqh_id), conn)
            return df.iloc[0].to_dict()


class RepoEdbQuoMysql(RepoEdb):
    def __init__(self, database):
        self._database = database

    def get_data(self, param: ParamEdbdata) -> pd.DataFrame:
        with self._database.with_conn() as conn:
            contract, field = param.gtjaqh_id.split(':')
            condition = _se_condition(param.start_date, param.end_date)
            sql = "select date, %s as value from gresearch_china_day_quotation.china_future_day_quotation " \
                  "where contract='%s' %s " \
                  "order by date" % (field, contract, condition)
            data = pd.read_sql(sql, conn)
            data['value'] = data['value'].apply(lambda x: float(x))
            return data

    def get_data_detail(self, param: ParamEdbdata) -> pd.DataFrame:
        with self._database.with_conn() as conn:
            contract, field = param.gtjaqh_id.split(':')
            condition = _se_condition(param.start_date, param.end_date)
            sql = "select date, %s as value, 0 as serial, create_dt from gresearch_china_day_quotation.china_future_day_quotation " \
                  "where contract='%s' %s " \
                  "order by date" % (field, contract, condition)
            data = pd.read_sql(sql, conn)
            data['value'] = data['value'].apply(lambda x: float(x))
            return data

    def get_info(self, param: ParamGtjaqhid) -> dict:
        rst = dict()
        rst['gtjaqh_id'] = param.gtjaqh_id
        rst['name'] = param.gtjaqh_id
        rst['unit'] = ''
        rst['freq'] = ''
        rst['data_source'] = "国泰君安期货"
        return rst


# _service edb ----------------------------------------------------------------------------------------------------------
class ServiceEdb:
    def get_data(self, param: ParamEdbdata) -> pd.DataFrame:
        raise Exception()

    def get_data_detail(self, param: ParamEdbdata) -> pd.DataFrame:
        raise Exception()

    def get_info(self, param: ParamGtjaqhid) -> dict:
        raise Exception()


# _service edb mysql ----------------------------------------------------------------------------------------------------
class ServiceEdbMysql(ServiceEdb):
    # 经济指标数据库查询
    def __init__(self, database, repo_edb: RepoEdb = None, repo_edb_quo: RepoEdb = None):
        self._repo_edb = repo_edb if repo_edb else RepoEdbMysql(database)
        self._repo_edb_quo = repo_edb_quo if repo_edb_quo else RepoEdbQuoMysql(database)

    def get_data(self, param: ParamEdbdata) -> pd.DataFrame:
        tmp = param.gtjaqh_id.replace("：", ":").replace(" ", "").split(":")
        if len(tmp) == 2:
            return self._repo_edb_quo.get_data(param)
        else:
            return self._repo_edb.get_data(param)

    def get_data_detail(self, param: ParamEdbdata) -> pd.DataFrame:
        tmp = param.gtjaqh_id.replace("：", ":").replace(" ", "").split(":")
        if len(tmp) == 2:
            return self._repo_edb_quo.get_data_detail(param)
        else:
            return self._repo_edb.get_data_detail(param)

    def get_info(self, param: ParamGtjaqhid) -> dict:
        tmp = param.gtjaqh_id.replace("：", ":").replace(" ", "").split(":")
        if len(tmp) == 2:
            return self._repo_edb_quo.get_info(param)
        else:
            return self._repo_edb.get_info(param)


# _service edb http -----------------------------------------------------------------------------------------------------
import requests
import json


def http(url: str, post_data: dict = None, headers: dict = None):
    if post_data is None:
        if headers:
            rst = requests.get(url, headers=headers)
        else:
            rst = requests.get(url)
    else:
        if headers:
            rst = requests.post(url, json=post_data, headers=headers)
        else:
            rst = requests.post(url, json=post_data)

    if rst.status_code == 200:
        data = json.loads(rst.text)
        if 'code' in data and data['code'] == 0:
            return data['data']
        else:
            try:
                text = json.loads(rst.text)
            except:
                text = rst.text
            raise Exception(text)
    else:
        raise Exception(rst.status_code)


class ServiceEdbHttp(ServiceEdb):
    def __init__(self, url_prefix: str, headers: dict):
        self._url_prefix = url_prefix
        self._headers = headers

    def get_info(self, param: ParamGtjaqhid):
        post_data = dict(param)
        url = urljoin(self._url_prefix, "/dataapi/edbinfo")
        rst = http(url, post_data, self._headers)
        return rst

    def get_data(self, param: ParamEdbdata):

        gtjaqh_id = param.gtjaqh_id
        post_data = dict(gtjaqh_id=param.gtjaqh_id)
        if param.start_date:
            post_data['start_date']= str(param.start_date)
        if param.end_date:
            post_data['end_date']= str(param.end_date)
        url = urljoin(self._url_prefix, "/dataapi/edb")
        rst = http(url, post_data, self._headers)

        if len(rst) > 0:
            rst = pd.DataFrame(rst)
            tmp = gtjaqh_id.split(":")
            if len(tmp) == 2:
                rst.columns = ['date', 'value']
            rst['value'] = rst['value'].apply(lambda x: float(x))
            rst['date'] = pd.to_datetime(rst['date']).apply(lambda x: x.date())
            return rst
        else:
            return []

    def get_data_detail(self, param: ParamEdbdata):
        gtjaqh_id = param.gtjaqh_id
        post_data = dict(gtjaqh_id=param.gtjaqh_id)
        if param.start_date:
            post_data['start_date']= str(param.start_date)
        if param.end_date:
            post_data['end_date']=str(param.end_date)
        url = urljoin(self._url_prefix, "/dataapi/edb")
        rst = http(url, post_data, self._headers)

        url = urljoin(self._url_prefix, "/dataapi/edbdetail")
        rst = http(url, post_data, self._headers)
        rst = pd.DataFrame(rst)
        tmp = gtjaqh_id.split(":")
        # if len(tmp) == 2:
        #    rst.columns = ['date', 'value']
        rst['value'] = rst['value'].apply(lambda x: float(x))
        rst['date'] = pd.to_datetime(rst['date']).apply(lambda x: x.date())
        rst = rst.sort_values("date")
        rst.index = range(len(rst))
        return rst

    def get_edb_menu(self):
        url = urljoin(self._url_prefix, "/dataapi/edbmenu")
        rst = http(url, headers=self._headers)
        return pd.DataFrame(rst)





