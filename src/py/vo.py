# -*-coding:utf-8-*-

"""
视图对象

@author Myles Yang
"""
import traceback
import typing
from enum import Enum

from starlette.responses import JSONResponse


class ConfigVO(object):
    """  """
    key: str
    value: typing.Any
    pytype: type
    defaults: typing.Any  # 默认值，pcikle序列化字节字符串值
    comment: str
    enable: bool
    utime: str
    ctime: str

    def __init__(self,
                 key: str = None,
                 value: typing.Any = None,
                 enable: bool = None
                 ):
        self.key = key
        self.value = value
        self.enable = enable
        self.pytype = type(value).__name__
        self.defaults = None
        self.comment = ''
        self.enable = True


class StatusVO(object):
    """  """
    running: bool


class RS(Enum):
    """ 自定义响应状态 """

    NOT_CURRENT_CLIENT = (401, '非最近请求客户端')
    NOT_FOUND = (404, '请求目标不存在')


class E(Exception):
    """
    自定义异常
    """
    status = 400
    message = 'error'
    cause = ''
    data = None

    def rs(self, rs: RS, data: typing.Any = None):
        self.status = rs.value[0]
        self.message = rs.value[1]
        self.data = data
        return self

    def ret(self, status: int = 400, message: str = None, data: typing.Any = None):
        self.status = status
        self.message = message
        self.data = data
        return self

    def e(self, e: Exception, message: str = None, data: typing.Any = None):
        tb = traceback.format_tb(e.__traceback__)
        if tb:
            self.cause = tb[0]
        self.message = message if message else e.__str__()
        self.data = data
        return self


class R(object):
    """
    自定义返回体
    """

    content = {
        'status': 200,
        'message': 'success',
        'data': None
    }

    def ok(self, message: str = 'success', data: typing.Any = None):
        self.content['status'] = 200
        self.content['message'] = message
        self.content['data'] = data
        return JSONResponse(content=self.content)

    def err(self, message: str = 'fail', data: typing.Any = None):
        self.content['status'] = 400
        self.content['message'] = message
        self.content['data'] = data
        return JSONResponse(content=self.content)

    def rs(self, rs: RS, data: typing.Any = None):
        self.content['status'] = rs.value[0]
        self.content['message'] = rs.value[1]
        self.content['data'] = data
        return JSONResponse(content=self.content)

    def ret(self, status: int, message, data: typing.Any = None):
        self.content['status'] = status
        self.content['message'] = message
        self.content['data'] = data
        return JSONResponse(content=self.content)

    def e(self, e: E):
        self.content['status'] = e.status
        self.content['message'] = e.message
        self.content['data'] = e.data
        return JSONResponse(content=self.content)
