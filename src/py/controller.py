# -*-coding:utf-8-*-

"""
控制器

@author Myles Yang
"""

import base64
import io
import json
import os

import win32con
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import StreamingResponse, RedirectResponse

import application
import configurator as configr
import const_config as const
import dao
import service
import utils
from component import AppBreathe, CustomLogger
from vo import R

log = CustomLogger().get_logger()

# 路由根路径
index = APIRouter()

# 路由 api
api = APIRouter(prefix="/api")

app_breathe: AppBreathe = None  # 服务端心跳维持


def init_app_breathe():
    """ 初始化 app 心跳行为，在webui服务启动时初始化 """
    log.info("初始化 App 心跳行为")

    def cb():
        log.info('WEBUI长时间无操作，自动退出程序')
        configr.record_fpid(False)
        utils.kill_process([os.getpid(), utils.getpid()])

    global app_breathe
    app_breathe = AppBreathe(60, 5)
    app_breathe.run(callback=cb)
    return app_breathe


"""===================== INDEX ====================="""


@index.get("/favicon.ico")
async def favicon():
    return StreamingResponse(
        content=io.BytesIO(base64.b64decode(const.favicon)),
        media_type='image/x-icon'
    )


@index.get('/exit')
async def exit_webui():
    log.info('主动关闭WEBUI服务')
    configr.record_fpid(False)
    msg = utils.kill_process([os.getpid(), utils.getpid()])
    return R().ok(message='结束WEBUI服务端进程', data=msg)


@index.get("/")
async def home():
    return RedirectResponse('/webui')


@index.get("/webui")
async def webui():
    if not os.path.exists(os.path.join(const.app_dirname, 'webui', 'index.html')):
        utils.create_dialog("WEBUI组件缺失！", const.dialog_title,
                            style=win32con.MB_ICONERROR, interval=7,
                            callback=lambda x: utils.kill_process([os.getpid(), utils.getpid()]))
        return R().err('WEBUI组件缺失')
    return RedirectResponse('/webui/index.html')


"""===================== API ====================="""


@api.get("/breathe")
async def breathe():
    """ APP心跳 """
    return R().ok(message='APP心跳', data=app_breathe.record_alive())


@api.get("/config")
async def get_config():
    """ 获取配置信息 """
    config = dao.list_config_kv()
    return R().ok(message='获取配置信息', data=config)


@api.post("/config")
async def update_config(request: Request):
    """ 更新配置信息 """
    json = await request.json()
    service.update_config(json)
    return R().ok(message='更新配置信息')


@api.get("/toggle-ud")
async def toggle_ud():
    """ toggle startup-shutdown 切换程序开关 """
    status = service.toggle_startup_shutdown()
    return R().ok(message='程序状态信息', data=status.__dict__)


@api.get("/config/workdir")
def get_workdir():
    """ 选择工作目录 """
    path = utils.select_folder('请选择工作目录')
    return R().ok('工作目录', path)


@api.get("/status")
async def get_status():
    """ 获取状态信息 """
    status = service.get_status()
    return R().ok(message='程序状态信息', data=status.__dict__)


@api.get("/create-desktop-lnk")
async def create_desktop_lnk():
    """ 创建程序桌面快捷方式 """
    utils.create_shortcut(application.app_fullpath, 'shell:desktop:{}'.format(const.app_name), style=7)
    return R().ok(message='创建桌面快捷方式')


@api.get("/locate-favorite-path")
async def locate_favorite_path():
    """ 打开收藏文件夹 """
    service.locate_favorite_path()
    return R().ok(message='打开收藏文件夹')


@api.get("/locate-workdir")
async def locate_workdir():
    """ 打开工作目录 """
    service.locate_workdir()
    return R().ok(message='打开工作目录')


@api.post("/wallhaven")
async def get_wallhaven(request: Request):
    """ wallhaven接口数据，因为前端直接请求会产生跨域，直接后端请求返回 """
    params = await request.json()
    resp = utils.simple_request_get(const.wallhaven_api, params=params)
    result = resp.text
    if resp.status_code == 200:
        return R().ok(message='wallhaven数据', data=json.loads(result))
    else:
        return R().err(message=result)
