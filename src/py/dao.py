# -*-coding:utf-8-*-

"""
持久层

@author Myles Yang
"""
import os
import re
import sqlite3
import typing
from sqlite3 import Cursor
from typing import Union, List, Dict

import const_config as const
import utils
from vo import E, ConfigVO


def run_sql(cb):
    """
    执行 SQL
    :param cb: 回调函数，参数 Cursor
    :return: None
    """

    con = None
    cur = None
    try:
        con = sqlite3.connect(os.path.join(const.app_dirname, const.db_name))
        cur = con.cursor()
        res = cb(cur)
        con.commit()
        return res
    except Exception as e:
        if con:
            con.rollback()
        raise E().e(e, message="读取或修改配置信息错误")
    finally:
        if cur:
            cur.close()
        if con:
            con.close()


def init_db():
    """ 初始化默认数据库 """
    utils.rm_file_dir(const.db_name)
    with open(const.db_name, 'wb'):
        pass

    def cb(cur: Cursor):
        cur.executescript(const.db_init_sql)
        return cur.rowcount

    return run_sql(cb)


def __str_escape(value: str):
    """ SQL 特殊字符转义 """
    value = str(value)
    value = value.replace("'", "''")
    # value = value.replace("/", "//")
    # value = value.replace("[", "/[")
    # value = value.replace("]", "/]")
    # value = value.replace("%", "/%")
    # value = value.replace("&", "/&")
    # value = value.replace("_", "/_")
    # value = value.replace("(", "/(")
    # value = value.replace(")", "/)")
    return value


def __get_pytype(pytype: str):
    """ 转换失败返回None """
    tpy = [None]
    try:
        if pytype and re.match('^(int|float|bool|complex|str|tuple|list|set|dict|type)$', pytype):
            exec('tpy[0]={}'.format(pytype))
        else:
            raise Exception('转换失败')
    except:
        tpy = [None]
    return tpy[0]


def __is_direct_type(typename: str):
    return typename and re.match('^(int|float|complex|bool|str)$', typename)


def __get_true_value(key: str, str_value: str, pytype: Union[type, str] = None) -> typing.Any:
    """ 获取配置健的真实值 """
    try:
        if pytype is None:
            tpy = str
        # 基本数值类型，直接转换
        elif isinstance(pytype, type) and __is_direct_type(pytype.__name__):
            tpy = pytype
        else:
            tpy = __get_pytype(pytype.__name__ if isinstance(pytype, type) else str(pytype))

        if not isinstance(str_value, str):
            result = str_value
        elif tpy == bool:
            result = str_value.lower() == 'true'
        elif tpy is not None and re.match('^(int|float|complex|bool|str)$', tpy.__name__):
            result = tpy(str_value)
        else:
            try:
                result = utils.deserialize(str_value)
            except:
                result = str(str_value)
    except Exception as e:
        raise E().e(e, message='获取配置健的真实值错误,k[{}],v[{}],t[{}]'.format(key, str_value, pytype))
    return result


def __get_result(result: dict) -> ConfigVO:
    """ 获取结果集，转成ConfigVO """
    result = result if result else {}
    vo = ConfigVO()

    key = str(result.get('key'))
    value = str(result.get('value'))
    enable = str(result.get('enable'))
    defaults = result.get('defaults')

    vo.key = key
    vo.value = __get_true_value(key, value, result.get('pytype'))
    vo.pytype = __get_pytype(result.get('pytype'))
    vo.defaults = utils.deserialize(defaults) if defaults is not None else defaults
    vo.enable = enable and enable != '0'
    vo.comment = result.get('comment')
    vo.utime = result.get('utime')
    vo.ctime = result.get('ctime')
    return vo


def kv2dict(data: dict) -> dict:
    """
    数据库key-value转字典，如{'run.api': ''} -> {'run':{api:''}}
    :param data: 数据库查询出来的键值对
    :return:
    """
    res = {}
    try:
        for key in data:
            value = data.get(key)
            get_statement = 'res'
            set_statement = 'res'
            for dict_key in key.split('.'):
                get_statement += ".get('{}')".format(dict_key)
                set_statement += "['{}']".format(dict_key)
                if not eval(get_statement):
                    exec(set_statement + '={}')
            exec(set_statement + '=value')
    except Exception as e:
        raise E().e(e, message='数据转换出错')
    return res


def dict2kv(data: dict) -> dict:
    """
    字典转数据库key-value，如{'run':{api:''}} -> {'run.api': ''}
    :param data: 前端传回来的配置项
    :return:
    """

    def recursion(key: str, rdt: dict, res: dict):
        for k in rdt:
            cur_key = key + ('.' if key else '') + k
            if isinstance(rdt[k], dict):
                recursion(cur_key, rdt[k], res)
            else:
                res[cur_key] = rdt[k]

    result = {}
    try:
        recursion('', data, result)
    except Exception as e:
        raise E().e(e, message='数据转换出错')
    return result


def list_config(enable: bool = None, like_key: str = None) -> Dict[str, ConfigVO]:
    """
    列出所有配置信息
    :return: {k:ConfigVO,}
    """

    def cb(cur: Cursor):
        sql = "select key, value, pytype, defaults, enable, comment, utime, ctime from config where 1=1 {} {};".format(
            "and enable = {}".format(1 if enable else 0) if enable is not None else "",
            "and key like '{}'".format(like_key) if like_key else ""
        )
        cur.execute(sql)
        res = {}
        for row in cur.fetchall():
            res[row[0]] = __get_result({
                'key': row[0],
                'value': row[1],
                'pytype': row[2],
                'default': row[3],
                'enable': row[4],
                'comment': row[5],
                'utime': row[6],
                'ctime': row[7],
            })
        return res

    return run_sql(cb)


def list_config_kv(enable: bool = None, like_key: str = None) -> dict:
    """
    列出所有配置信息
    :return: {k:v,}
    """
    config = list_config(enable, like_key)
    res = {}
    for key in config:
        vo = config.get(key)
        res[key] = vo.value

    return kv2dict(res)


def list_config_ko(enable: bool = None, like_key: str = None) -> dict:
    """
    列出所有配置信息
    :return: {k:ConfigVO,}
    """
    config = list_config(enable, like_key)
    return kv2dict(config)


def update_config(data: List[ConfigVO], merge: bool = False) -> int:
    """
    更新配置信息
    :rtype: object
    :param data: [{key,value,enable},{key,value}...]
    :param merge: 是否为 merge 模式：delete -> insert
    :return: 生效数目
    """

    def cb(cur: Cursor):
        res = 0
        for vo in data:
            key = vo.key
            value = vo.value
            pytype = type(value).__name__
            enable = vo.enable

            update_sql = "update config set key = key {} {} {} where key = '{}';".format(
                ",value = '{}'".format(
                    __str_escape(value) if __is_direct_type(pytype) else __str_escape(utils.serialize(value))),
                ",pytype = '{}'".format(pytype),
                ",enable = {}".format(1 if enable else 0) if enable is not None else '',
                __str_escape(key)
            )
            cur.execute(update_sql)
            res += cur.rowcount

            if merge:
                merge_sql = "insert into config(key, value, pytype, enable) select '{}', '{}', '{}', {} where (select changes() = 0);".format(
                    __str_escape(key),
                    __str_escape(value) if value is not None else '',
                    pytype if value is not None else '',
                    (1 if enable else 0) if enable is not None else 1,
                )
                cur.execute(merge_sql)
                res += cur.rowcount
        return res

    return run_sql(cb)


def get_config(key: str, enable: bool = None) -> ConfigVO:
    """
    获取单个配置项
    :param key: key
    :param enable: 是否有效
    :return: 配置项值
    """

    def cb(cur: Cursor):
        sql = "select value, pytype, defaults, enable, comment, utime, ctime " \
              "from config where key = '{}' {};".format(
            key,
            '' if enable is None else 'and enable = {}'.format(1 if enable else 0)
        )
        cur.execute(sql)
        res = cur.fetchone()

        return __get_result({
            'key': key,
            'value': res[0],
            'pytype': res[1],
            'defaults': res[2],
            'enable': res[3],
            'comment': res[4],
            'utime': res[5],
            'ctime': res[6],
        }) if res else None

    return run_sql(cb)


def delete_config(key: Union[List[str], str]) -> int:
    """
    删除配置项目
    :param key: key列表，或字符串(使用like，如'key%')
    :return: 生效数目
    """

    def cb(cur: Cursor):
        if isinstance(key, list):
            incondition = ''
            for k in key:
                incondition += "'{}',".format(k)
            if incondition:
                incondition = incondition.rstrip(',')
            sql = "delete from config where key in ({});".format(incondition)
            cur.execute(sql)
        elif isinstance(key, str):
            sql = "delete from config where key like '{}';".format(key)
            cur.execute(sql)
        return cur.rowcount

    return run_sql(cb)


def add_config(data: List[ConfigVO]) -> int:
    """
    添加配置项
    :param data: [{key,value}...]
    :return: 生效数目
    """

    def cb(cur: Cursor):
        res = 0
        for vo in data:
            value = vo.value
            pytype = type(value).__name__
            defaults = vo.defaults
            enable = vo.enable
            comment = vo.comment

            sql = "insert into config(key, value, pytype, defaults, enable, comment) values('{}', '{}', '{}', '{}', {}, '{}')".format(
                __str_escape(vo.key),
                __str_escape(value) if __is_direct_type(pytype) else __str_escape(utils.serialize(value)),
                pytype,
                __str_escape(utils.serialize(defaults)),
                1 if enable is None else (1 if enable else 0),
                __str_escape(comment) if comment is not None else '',
            )
            cur.execute(sql)
            res += cur.rowcount
        return res

    return run_sql(cb)
