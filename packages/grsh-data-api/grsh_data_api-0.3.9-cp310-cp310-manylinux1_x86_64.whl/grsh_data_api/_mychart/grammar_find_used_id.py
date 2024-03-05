# 数据二次计算grammmar
# 支持取数据方法
#   DATA
#   DATA_SEASON 季节性，支持参数：
#     (season_start_date "10-01")  (season_year "2023/22,2022/21")
#     (season_year "2023,2022")
#   DATA_LUNAR_SEASON


import abc
import datetime

import dateutil
import pandas as pd
from typing import Union, List
from grsh_data_api import _get_global_var
from grsh_data_api.base import Serie
from grsh_data_api._service import get_service_edb
from grsh_data_api.util import Tool
from grsh_data_api._mychart.h_grammar_to_list import grammar_to_list
from grsh_data_api._service.edb import ParamGtjaqhid, ParamEdbdata


class CalculateMock:
    # 基于Serie的结构，实现指标的二次计算
    @staticmethod
    def serie(gtjaqh_id: str, option: dict) -> Serie:
        try:
            start_date = option.get("start_date", None)
            end_date = option.get("end_date", None)
            if start_date:
                start_date = dateutil.parser.parse(start_date).date()
            if end_date:
                end_date = dateutil.parser.parse(end_date).date()

            # edb quo（contract:field  单个field的形式） 统一用一个接口

            # create _service edb obj
            #global_var = _get_global_var()
            #service_edb = get_service_edb()
            #if service_edb['name'] == 'http':
            #    obj = service_edb['class_obj'](url_prefix=global_var['url'], headers=global_var['headers'])
            #elif service_edb['name'] == 'mysql':
            #    obj = service_edb['class_obj'](service_edb['option']['database'])

            # query
            #p1 = ParamEdbdata(gtjaqh_id=gtjaqh_id, start_date=start_date, end_date=end_date)
            #p2 = ParamGtjaqhid(gtjaqh_id=gtjaqh_id)
            #df = obj.get_data(p1)
            #info = obj.get_info(p2)

            df = pd.DataFrame([dict(date=datetime.date(2022,7,1), value=1.1),
                               dict(date=datetime.date(2023,2,1), value=1.2)])
            info = dict(gtjaqh_id='mock', name='mock')

            s = Serie(df, **info)
            if 'name' in option:
                s.name = option['name']
            if 'unit' in option:
                s.unit = option['unit']
            #return s
            #data = obj.query(ParamEdbdata(gtjaqh_id=gtjaqh_id, start_date=start_date, end_date=end_date), option)
            return CalculateMock.adjust_with_option(s, option)

        except Exception as e:
            print(str(e))
            import traceback
            traceback.print_exc()
            raise Exception("数据错误")

    @abc.abstractmethod
    def parse(self) -> List:
        pass

    @staticmethod
    def handle_num_op(d1: Union[Serie, float], d2: Union[Serie, float], op: str) -> Union[None, float]:
        if (not isinstance(d1, Serie)) and (not isinstance(d2, Serie)):
            # d1 = float(d1)
            # d2 = float(d2)
            if op == "+":
                return d1 + d2
            elif op == "*":
                return d1 * d2
            elif op == "-":
                return d1 - d2
            elif op == "/":
                return d1 / d2
        return None

    @staticmethod
    def init_data(d1: Union[Serie, float], d2: Union[Serie, float]) -> tuple[Serie, Serie]:
        # 在四则运算之前做预处理
        # d1 d2中必须有一个是Serie对象
        # 将非Serie对象转换为Serie对象，info保持一直
        if (not isinstance(d1, Serie)) and (not isinstance(d2, Serie)):
            raise Exception("d1 d2 must has one GSeries object")
        if not isinstance(d1, Serie):
            d1 = Serie.create_from_num(d1, d2)
        if not isinstance(d2, Serie):
            d2 = Serie.create_from_num(d2, d1)
        return d1, d2

    @staticmethod
    def adjust_with_option(serie: Serie, option: dict) -> Serie:
        if option:
            for k in option:
                if k in ['name', 'unit', 'freq', 'data_source']:
                    setattr(serie, k, option[k])
            if 'remove_date' in option:
                try:
                    # print("\tdebug: remove date", option['remove_date'])
                    remove_date_lst = [pd.to_datetime(i).date() for i in
                                       option['remove_date'].replace(" ", "").split(",")]
                    serie.df = serie.df[~serie.df['date'].isin(remove_date_lst)].reset_index(drop=True)
                    return serie
                except Exception as e:
                    raise Exception("invalid remove date input %s" % e)

        return serie

    @staticmethod
    def op_add(data_list: List, option: dict = None) -> Serie:
        assert len(data_list) >= 2
        rst = data_list[0]
        for i in range(1, len(data_list)):
            tmp = data_list[i]
            _rst = CalculateMock.handle_num_op(rst, tmp, "+")
            if _rst:
                rst = _rst
            else:
                d1, d2 = CalculateMock.init_data(rst, tmp)
                rst = d1 + d2
        return CalculateMock.adjust_with_option(rst, option)

    @staticmethod
    def op_mul(data_list: List, option: dict = None) -> Serie:
        assert len(data_list) >= 2
        rst = data_list[0]
        for i in range(1, len(data_list)):
            tmp = data_list[i]
            _rst = CalculateMock.handle_num_op(rst, tmp, "*")
            if _rst:
                rst = _rst
            else:
                d1, d2 = CalculateMock.init_data(rst, tmp)
                rst = d1 * d2
        return CalculateMock.adjust_with_option(rst, option)

    @staticmethod
    def op_sub(data_list: List, option: dict = None):
        if len(data_list) == 1:
            return CalculateMock.op_mul([data_list[0], -1])
        else:
            rst = data_list[0]
            for i in range(1, len(data_list)):
                tmp = data_list[i]
                _rst = CalculateMock.handle_num_op(rst, tmp, "-")
                if _rst:
                    rst = _rst
                else:
                    d1, d2 = CalculateMock.init_data(rst, tmp)
                    rst = d1 - d2
            return CalculateMock.adjust_with_option(rst, option)

    @staticmethod
    def op_div(data_list: List, option: dict = None) -> Serie:
        assert len(data_list) >= 2
        rst = data_list[0]
        for i in range(1, len(data_list)):
            tmp = data_list[i]
            _rst = CalculateMock.handle_num_op(rst, tmp, "/")
            if _rst:
                rst = _rst
            else:
                d1, d2 = CalculateMock.init_data(rst, tmp)
                rst = d1 / d2
        return CalculateMock.adjust_with_option(rst, option)

    @staticmethod
    def resample(data_list: List, option: dict = None) -> Serie:
        freq = option['freq'].upper()
        assert freq in ['W', 'M', 'Y']
        assert len(data_list) == 1

        d1 = data_list[0]
        df = d1.df.copy()
        df['date'] = pd.to_datetime(df['date'])  # convert date -> timpstamp
        df = df.set_index("date")
        df = df['value'].resample(freq).last()
        df = df.reset_index()
        df['date'] = df['date'].apply(lambda x: x.date())
        df = Tool.df_fill_to_end(df, 'value')

        nd = Serie(df, d1.gtjaqh_id, d1.name, d1.data_source, d1.unit, d1.freq)
        for k in option:
            if k in ['name', 'unit', 'freq', 'data_source']:
                setattr(nd, k, option[k])
        return nd

    @staticmethod
    def shift(data_list: List, option: dict = None) -> Serie:
        assert len(data_list) == 1
        d1 = data_list[0]
        period = int(option['period'])
        df = d1.df.copy()
        df = df.set_index("date")
        df = df.shift(period)
        df = df.dropna()
        df = df.reset_index()
        nd = Serie(df, d1.gtjaqh_id, d1.name, d1.data_source, d1.unit, d1.freq)
        for k in option:
            if k in ['name', 'unit', 'freq', 'data_source']:
                setattr(nd, k, option[k])
        return nd

    @staticmethod
    def ma(data_list: List, option: dict = None) -> Serie:
        assert len(data_list) == 1
        d1 = data_list[0]
        return d1


class SexpMock:
    _SUPPORT_OP = {
        "SERIE": CalculateMock.serie,
        'RESAMPLE': CalculateMock.resample,
        'SHIFT': CalculateMock.shift,
        '+': CalculateMock.op_add,
        '-': CalculateMock.op_sub,
        '*': CalculateMock.op_mul,
        '/': CalculateMock.op_div,
        'MA': CalculateMock.ma
    }

    def __init__(self, grammar: str):
        self._grammar = grammar  # 原始grammar
        self._grammar_list = None  # 解析后的
        self._info = None
        self._type_name = None
        self._data_series = None
        self._param = None
        self._grammar_list = grammar_to_list(grammar)

        self._used_id_lst = []

        # 处理数据
        self._handle()


    def _handle_data_series(self, data):
        def _check_is_serie(lst):
            if lst[0] in self._SUPPORT_OP:
                return True
            else:
                return False

        def _check_is_num(num):
            try:
                float(num)
                return True
            except:
                return False

        if isinstance(data, list):
            if data[0] == 'SERIE':
                func = data[0]
                d1 = data[1]
                # 使用var做替换
                if d1.upper().startswith("VAR") and d1 in self._var:
                    d1 = self._var[d1]

                self._used_id_lst.append(d1)

                option = {}
                for v in data[2:]:
                    option[v[0]] = v[1]
                return self._SUPPORT_OP[func](d1, option)
            else:
                func = data[0]
                # loop_to_end_with_all_serie = False
                for i in range(1, len(data)):
                    if not (_check_is_serie(data[i]) or _check_is_num(data[i])):
                        i = i - 1
                        break
                data_list = [self._handle_data_series(v) for v in data[1:(i + 1)]]
                option = {}
                for v in data[(i + 1):]:
                    option[v[0]] = v[1]
                return self._SUPPORT_OP[func](data_list, option)
        else:
            if isinstance(data, Serie):
                return data
            elif isinstance(data, str):
                return float(data)

    def _handle(self):
        rst = self._grammar_list
        # pprint.pprint(rst)

        # 提取参数 （chart_type_name (chart_data_series) 其他参数）
        type_name = rst[0][0]
        _data_series = rst[0][1]
        param = dict()
        var = dict()
        for item in rst[0][2:]:
            if item[0] == 'SETVAR':
                if isinstance(item[1], str):
                    if len(item) == 3:
                        var[item[1]] = item[2]
                    else:
                        raise Exception(f"please check {item}")
                else:
                    for pair in item[1:]:
                        if len(pair) == 2:
                            var[pair[0]] = pair[1]
                        else:
                            raise Exception(f"please check {item}")
            else:
                param[item[0]] = item[1]

        self._type_name = type_name
        self._param = param
        self._var = var

        # 解析具体的数据序列
        data_series = []
        MAX_ALLOW_DATA_LEN = 15

        def _add_data_serie(_ds):
            if len(data_series) >= MAX_ALLOW_DATA_LEN:
                raise Exception(f"max allow data len = {MAX_ALLOW_DATA_LEN}")
            data_series.append(_ds)

        info = []
        if not isinstance(_data_series[0], list):
            # single data, 第一个元素为op操作符
            obj = self._handle_data_series(_data_series)
            _add_data_serie(obj)
            # data_series.append(obj)
            info.append(obj.info_2_dict())
        else:
            # multi
            for v in _data_series:
                obj = self._handle_data_series(v)
                _add_data_serie(obj)
                # data_series.append(obj)
                info.append(obj.info_2_dict())

        _cache_name = set()
        for item in data_series:
            if item.name not in _cache_name:
                _cache_name.add(item.name)
            else:
                for i in range(30):
                    n_name = item.name + f"_{i}"
                    if n_name not in _cache_name:
                        item.name = n_name
                        _cache_name.add(n_name)
                        break

        self._data_series = data_series
        self._info = info

    def get_result(self):
        return dict(
            grammar=self._grammar,
            type_name=self._type_name,
            serie_lst=self._data_series,
            param=self._param,
            var=self._var
        )

    def get_used_id_lst(self):
        return self._used_id_lst


if __name__ == "__main__":
    grammar = '''
    
(LINE_SINGLE 
  ( - (SERIE cu_index:close (start_date 20180101))
    ( +
     (* 1.65 (/(SERIE ID001473) 0.92))
     (* 0.5(/(SERIE ID026017) 0.93))
     1050) 
     
     (name "热卷加工利润")   
     (unit "吨")
  )
)
    '''
    obj = SexpMock(grammar)
    print(obj.get_result())
    print(obj._used_id_lst)

