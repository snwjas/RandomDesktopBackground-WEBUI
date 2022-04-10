# -*-coding:utf-8-*-

"""
业务逻辑

@author Myles Yang
"""
import os
import time
from typing import List

import application as app
import args_definition as argsdef
import configurator as configr
import const_config as const
import dao
import utils
from vo import E, ConfigVO, StatusVO


def get_status():
    """ 获取程序状态 """
    status = StatusVO()

    # 运行状态
    bpid = configr.get_bpid()
    status.running = bpid and utils.is_process_running(bpid, app.app_fullpath)

    return status


def toggle_startup_shutdown():
    """ 切换程序开关 """

    def check_running_status(running: bool):
        loop = 60  # 30 seconds allowable check time
        while loop > 0:
            bpid = configr.get_bpid()
            if running:
                if bpid and utils.is_process_running(bpid, app.app_fullpath):
                    break
            else:
                if bpid and not utils.is_process_running(bpid, app.app_fullpath):
                    break
            time.sleep(0.5)
            loop -= 1

    bpid = configr.get_bpid()
    if bpid and utils.is_process_running(bpid, app.app_fullpath):
        configr.record_bpid(False)
        utils.kill_process([bpid])
        check_running_status(False)
    else:
        args = ' {} {} {} {}'.format(argsdef.ARG_RUN, argsdef.ARG_RUN_TYPE_BACKGROUND,
                                     argsdef.ARG_LOG, argsdef.ARG_LOG_TYPE_FILE)
        succeed, msg = utils.run_in_background(app.app_fullpath, args)
        if succeed:
            check_running_status(True)
    return get_status()


def update_config(config: dict):
    """ 更新配置信息（暂不做参数检验） """
    try:
        config = dao.dict2kv(config)
        update_list: List[ConfigVO] = []
        for k in config:
            update_list.append(ConfigVO(k, config.get(k)))

        # 自定义图源，先删除再添加
        api_name = config.get(const.Key.Api.NAME.value)
        if api_name == const.Key.Api._NAME_CUSTOM.value:
            dao.delete_config('{}%'.format(const.Key.Api.CUSTOM.value))

        ures = dao.update_config(update_list, merge=True)
        if ures > 0:
            # 开机启动
            run_startup = config.get(const.Key.Run.STARTUP.value)
            if run_startup is not None:
                create_startup_lnk() if run_startup else delete_startup_lnk()
            # 桌面右键菜单
            create_desktop_context_menu(dao.list_config())

    except Exception as e:
        raise E().e(e, message="配置更新失败")


def create_startup_lnk(log_type: str = None):
    """
    创建快捷方式到用户开机启动目录: shell:startup
    """
    args = '{} {} {} {}'.format(argsdef.ARG_RUN, argsdef.ARG_RUN_TYPE_BACKGROUND,
                                argsdef.ARG_LOG, log_type if log_type else argsdef.ARG_LOG_TYPE_FILE)
    return utils.create_shortcut(app.app_fullpath, 'shell:startup:{}'.format(const.app_name), args=args, style=7)


def delete_startup_lnk():
    """ 删除开启自启快捷方式 """
    try:
        startup_path = utils.get_special_folders('startup')
        paths = os.listdir(startup_path)
        for path in paths:
            name, ext = os.path.splitext(path)
            if '.lnk' == ext.lower():
                lnkpath = os.path.join(startup_path, path)
                target_lnk_path = utils.get_shortcut(lnkpath)
                if os.path.normcase(target_lnk_path) == os.path.normcase(app.app_fullpath):
                    os.remove(lnkpath)
    except Exception as e:
        raise E().e(e, message="取消开机自启错误")


def locate_favorite_path():
    """ 打开收藏文件夹 """
    favorite_path = configr.get_favorite_abspath()

    if os.path.isdir(favorite_path):
        utils.locate_path(favorite_path, False)
    else:
        raise E().ret(message="收藏目录不存在：{}".format(favorite_path))


def locate_workdir():
    """ 打开工作目录 """
    workdir = configr.get_workdir()
    workdir = workdir if workdir else 'run'

    if os.path.isdir(workdir):
        utils.locate_path(workdir, False)
    else:
        raise E().ret(message="工作目录不存在：{}".format(workdir))


def create_desktop_context_menu(config=None):
    """ 删除 -> 添加 """
    utils.delete_desktop_context_menu(const.app_name_en)
    if not configr.is_ctxmenu_enabled(config): return

    prev = configr.is_ctxmenu_prev_enabled(config)
    next = configr.is_ctxmenu_next_enabled(config)
    fav = configr.is_ctxmenu_favorite_enabled(config)
    loc = configr.is_ctxmenu_locate_enabled(config)

    if not (prev or next or fav or loc): return

    def get_sub_menu(name, cmd, icon_idx, order):
        return [
            {
                'sub_key': '{}\\shell\\itm{}-{}'.format(const.app_name_en, order, cmd),
                'values': {
                    'Icon': '{},{}'.format(app.app_fullpath, icon_idx),
                    'MUIVerb': name,
                }
            },
            {
                'sub_key': '{}\\shell\\itm{}-{}\\command'.format(const.app_name_en, order, cmd),
                'values': {
                    '': '{} --run cmd --cmd {}'.format(app.app_fullpath, cmd),
                }
            }
        ]

    reg_to_create = []
    if prev:
        reg_to_create.append(('上一张壁纸', 'pre', 1, 1))
    if next:
        reg_to_create.append(('下一张壁纸', 'nxt', 2, 2))
    if fav:
        reg_to_create.append(('收藏当前壁纸', 'fav', 3, 3))
    if loc:
        reg_to_create.append(('定位当前壁纸', 'loc', 4, 4))

    if len(reg_to_create) == 1:
        data = reg_to_create[0]
        utils.create_desktop_context_menu(const.app_name_en, {
            'Icon': '{},{}'.format(app.app_fullpath, 0),
            'MUIVerb': data[0],
        })
        utils.create_desktop_context_menu(const.app_name_en + "\\command", {
            '': '{} --run cmd --cmd {}'.format(app.app_fullpath, data[1]),
        })
    else:
        utils.create_desktop_context_menu(const.app_name_en, {
            'Icon': '{},{}'.format(app.app_fullpath, 0),
            'MUIVerb': const.app_name,
            'SubCommands': ''
        })
        for tp in reg_to_create:
            for d in get_sub_menu(*tp):
                utils.create_desktop_context_menu(d['sub_key'], d['values'])
