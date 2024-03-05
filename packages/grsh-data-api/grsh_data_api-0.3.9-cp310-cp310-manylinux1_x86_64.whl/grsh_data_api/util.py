import datetime
import os
import platform
import re
import json
import sys
import time
import jwt
import ntplib
import requests
import numpy as np
import pandas as pd
from dateutil.parser import parse
from typing import Union

__license = False


def _verify_license():
    """检测license

    windows系统默认位置为~/license-grsh.dat；linux默认位置为/etc/gtjaqh/license-grsh.dat

    """

    global __license

    if __license:
        return

    def _check_time():
        client = ntplib.NTPClient()
        r = None
        try:
            r = client.request('pool.ntp.org', port='ntp', version=4, timeout=1)
            r = r.tx_time
        except:
            pass

        if r:
            if abs(time.time() - r) > 60 * 60 * 24 * 10:
                raise Exception("check machine time")

    _check_time()

    _key = """
-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE6Uf4LBheJZhocDcEMp0tu9Jt4Wkp
ROKxXYF+xu0AoPR/RI0EkgtTI8hEeNzB2j1YSZhcOhSUXvWxemzNJYSCQg==
-----END PUBLIC KEY-----    
        """
    try:
        if platform.platform().upper().startswith("WINDOWS"):
            license_filename = os.path.expanduser("~/license-grsh.dat")
        elif platform.platform().upper().startswith("LINUX"):
            license_filename = "/etc/gtjaqh/license-grsh.dat"
        else:
            raise Exception(f"unkown platform {platform.platform()}")
        unverified_license = open(license_filename, 'r').read()
        payload = jwt.decode(
            jwt=unverified_license,
            key=_key,
            verify=True,
            algorithms=["ES256"],
            audience="GOD",
            issuer="国泰君安期货",
            options={'require_exp': True, 'verify_exp': True, 'verify_iss': True, 'verify_aud': True}
        )
        sys.stdout.writelines("[frame模块]该软件由[{}]向[{}]渠道[{}]客户授权使用至[{}]\n".format(
            payload['iss'],
            payload['aud'],
            payload['sub'],
            datetime.datetime.fromtimestamp(payload['exp'])))

        __license = True
        return True
    except FileNotFoundError:
        sys.stderr.writelines("license文件缺失")
        sys.exit()
    except jwt.exceptions.DecodeError:
        sys.stderr.writelines("license格式错")
        sys.exit()
    except jwt.exceptions.InvalidIssuerError:
        sys.stderr.writelines("license签发错误")
        sys.exit()
    except jwt.exceptions.InvalidAudienceError:
        sys.stderr.writelines("license渠道错误")
        sys.exit()
    except jwt.exceptions.ExpiredSignatureError:
        sys.stderr.writelines("license已过期")
        sys.exit()
    except Exception as e:
        print(e)
        sys.stderr.writelines("license异常")
        sys.exit()


# _verify_license()


def urljoin(u1: str, u2: str):
    if u1.endswith("/") and u2.startswith("/"):
        return u1[:-1] + u2
    elif (not u1.endswith("/")) and (not u2.startswith("/")):
        return u1 + "/" + u2
    else:
        return u1 + u2


class Tool:
    @staticmethod
    def parse_date(date: [str, None]):
        if date is None:
            return None

        pat = re.compile("^[0-9]{8}$$")
        if pat.match(date):
            try:
                return parse(date).date()
            except:
                raise Exception("failed parse date %s" % date)
        else:
            raise Exception("not vaild date %s" % date)

    @staticmethod
    def list2str(lst: [list, str]) -> str:
        if isinstance(lst, str):
            return "@" + lst
        return "@" + "|".join([str(__v) for __v in lst])

    @staticmethod
    def df2json(df: pd.DataFrame):
        def _tmp(x):
            x = x.to_dict()
            for k in x:
                x[k] = str(x[k])
            return x

        return json.dumps(list(map(lambda x: _tmp(x[1]), df.iterrows())))

    @staticmethod
    def df2list(df: pd.DataFrame):
        df = df.fillna('')

        def _tmp(x):
            x = x.to_dict()
            for k in x:
                x[k] = str(x[k])
            return x

        return list(map(lambda x: _tmp(x[1]), df.iterrows()))

    @staticmethod
    def df_fill_to_end(df: pd.DataFrame, column: Union[str, int]):
        df = df.copy(deep=True)
        _date = df[df[column].notnull()].iloc[-1].name
        _date_pos = df.index.get_loc(_date)
        df[column].fillna(method='ffill', inplace=True)
        if _date_pos < len(df):
            df[column].iloc[_date_pos + 1:] = np.nan
        return df


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
            raise Exception(rst.text)
    else:
        raise Exception(rst.status_code)
