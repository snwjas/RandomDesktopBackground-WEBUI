# -*-coding:utf-8-*-

"""
WEB 服务器，使用fastapi

@author Myles Yang
"""
import os

import uvicorn
import win32con
from fastapi import FastAPI, Request, Response
from fastapi.exceptions import StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

import args_definition as argsdef
import configurator as configr
import const_config as const
import utils
from component import CustomLogger
from controller import index as index_router, api as api_router, init_app_breathe
from vo import R, RS, E

run_args = argsdef.arg_dict

log = CustomLogger().get_logger()

XToken = None  # 客户端唯一标识，仅允许一个客户端进行请求


def __init_logger():
    """ 初始化WEBUI Logger (说明：webui另起一个进程，日志单例失效)"""
    logger = CustomLogger()
    logger.set_logpath(configr.get_log_abspath())
    logger.use_file_logger()


# web服务启动回调
def __on_startup():
    log.info('WEBUI服务启动：{}'.format(const.server))
    init_app_breathe()
    if run_args.get(argsdef.ARG_KEY_ENV) == argsdef.ARG_ENV_TYPE_PROD:
        __open_webui()
    configr.record_fpid(True)


# web服务关闭回调，windwos杀死进程似乎不会发出信号，下面代码应该不会执行
def __on_shutdown():
    log.info('WEBUI服务关闭：{}'.format(const.server))
    configr.record_fpid(False)


app = FastAPI(title=const.app_name,
              on_startup=[__init_logger, __on_startup],
              on_shutdown=[__on_shutdown])

# webui静态资源映射
__webui_path = os.path.join(const.app_dirname, 'webui')
os.makedirs(__webui_path, exist_ok=True)
app.mount("/webui", StaticFiles(directory=__webui_path), name="webui")


def __open_webui():
    utils.open_url('{}/webui'.format(const.server))


@app.middleware("http")
async def interceptor(request: Request, call_next):
    """
    拦截器定义
    """
    if request.url.path.startswith('/api/'):  # 拦截api接口
        # 检查请求头
        global XToken
        x_init = request.headers.get('X-Init')
        if x_init:
            XToken = x_init
            return R().ok(message="设置客户端唯一标识", data=x_init)
        x_token = request.headers.get('X-Token')
        if not x_token or x_token != XToken:
            return R().rs(RS.NOT_CURRENT_CLIENT)
    response: Response = await call_next(request)
    return response


""" 跨域配置，必须置于拦截器之后，否则请求被拦截时无法携带允许跨域的请求头而出现跨域报错
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.exception_handler(StarletteHTTPException)
async def not_found(request: Request, exc):
    return R().rs(RS.NOT_FOUND, {'path': request.url.path})


@app.exception_handler(E)
async def error(request: Request, exc: E):
    log.error("请求路径：{}，错误：{}\n{}".format(request.url.path, exc.message, exc.cause))
    return R().e(exc)


# 路由注册
app.include_router(index_router)
app.include_router(api_router)


def run_app():
    # 检测服务是否可用
    try:
        resp = utils.simple_request_get(const.server)
        if resp and resp.status_code == 200:
            __open_webui()
            return
    except:
        pass
    try:
        # 进程启动
        if run_args.get(argsdef.ARG_KEY_ENV) == argsdef.ARG_ENV_TYPE_PROD:
            uvicorn.run("webapp:app", host=const.host, port=const.port)
        else:
            uvicorn.run("webapp:app", host=const.host, port=const.port, reload=True, debug=True)
    except Exception as e:
        log.error('WEBUI服务启动失败，{}'.format(e))
        utils.create_dialog("WEBUI服务启动失败！", const.dialog_title,
                            style=win32con.MB_ICONERROR, interval=7,
                            callback=lambda x: utils.kill_process([utils.getpid()]))
