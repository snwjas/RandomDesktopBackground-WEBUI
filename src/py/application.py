# -*-coding:utf-8-*-

"""
程序启动入口
@author Myles Yang
"""

import os
import platform
import sys

import win32con

import args_definition as argsdef
import configurator as configr
import const_config as const
import utils
import webapp
from component import CustomLogger
from get_background import GetBackgroundTask
from set_background import SetBackgroundTask
from vo import E

app_fullpath = os.path.abspath(sys.argv[0])
app_dirname = os.path.dirname(app_fullpath)

logger = CustomLogger()
log = logger.get_logger()


def run_in_the_console():
    """
    以控制台程序方式运行
    """
    log.info('程序启动，当前系统操作系统: {}-{}'.format(platform.platform(), platform.architecture()))
    try:

        config = configr.parse_config()
        bg_abspath_list = configr.get_bg_abspaths()

        gtask = GetBackgroundTask(config)
        stask = SetBackgroundTask(config, bg_abspath_list, gtask.run)

        gtask.init_task(stask)

        stask.run()

        # 记录运行中程序的PID
        configr.record_bpid()
    except Exception as e:
        exc = E().e(e)
        log.error("程序启动错误：{}\n{}".format(exc.message, exc.cause))

    # WEB服务进程会阻塞，使用线程启动
    # Thread(target=webapp.run_app).start()


def run_in_the_background(log_type: str = None):
    """
    以控制台程序方式在后台运行
    """
    app_path = app_fullpath
    # 值得注意的是，这里进入后台运行的方式应该是CONSOLE，因为是以控制台的方式后台运行的，
    # 如果为 BACKGROUND 的话，会造成递归调用，不断循环启动应用，主进程PID不断改变，无法停止应用。
    # main -> background -> 后台运行 -> main -> 开始循环递归
    args = ' {} {} {} {}'.format(argsdef.ARG_RUN, argsdef.ARG_RUN_TYPE_CONSOLE,
                                 argsdef.ARG_LOG, log_type if log_type else argsdef.ARG_LOG_TYPE_FILE
                                 )

    succeed, msg = utils.run_in_background(app_path, args)
    if not succeed:
        utils.create_dialog("后台启动程序失败:\n\n{}".format(msg),
                            const.dialog_title, style=win32con.MB_ICONWARNING)
    return succeed

    # run_in_the_console()
    # ct = win32api.GetConsoleTitle()
    # hd = win32gui.FindWindow(None, ct)
    # win32gui.ShowWindow(hd, win32con.SW_HIDE)


def run_on_startup(log_type: str = None):
    """
    开机时启动，默认以后台方式运行程序
    """
    # 创建快捷方式到用户开机启动目录: shell:startup
    from service import create_startup_lnk
    create_startup_lnk(log_type)
    # 后台运行
    return run_in_the_background(log_type)


def run_webui():
    """ 启动webui """
    args = ' {} {} {} {}'.format(argsdef.ARG_RUN, argsdef.ARG_RUN_TYPE_WEBUI,
                                 argsdef.ARG_LOG, argsdef.ARG_LOG_TYPE_NONE
                                 )
    succeed, msg = utils.run_in_background(app_fullpath, args)
    if not succeed:
        utils.create_dialog("后台启动WEBUI服务失败:\n\n{}".format(msg),
                            const.dialog_title, style=win32con.MB_ICONWARNING)


def check() -> bool:
    """ 程序启动检测
    :return: True 检查通过
    """
    import dao
    # 检测配置文件
    if not os.path.isfile(os.path.join(app_dirname, const.db_name)):
        btn_val = utils.create_dialog("配置文件缺失，是否使用默认配置启动？", const.dialog_title, style=win32con.MB_YESNO)
        if btn_val != win32con.IDYES:
            os._exit(1)
            return False
        # 加载默认配置
        dao.init_db()
    # 检测程序是否在运行
    arg_dict = argsdef.arg_dict
    if arg_dict.get(argsdef.ARG_KEY_RUN):
        try:
            if utils.is_process_running(configr.get_bpid()):
                utils.create_dialog("检测到程序在运行中，请勿重复启动！", const.dialog_title,
                                    style=win32con.MB_ICONERROR, interval=7,
                                    callback=lambda x: utils.kill_process([os.getpid(), utils.getpid()]))
                return False
        except:
            pass

    return True


def main():
    if not check():
        return
    # 初始化logger
    logger.set_logpath(configr.get_log_abspath())
    logger.use_file_logger()

    # 获取启动参数
    run_args = argsdef.arg_dict
    # 创建程序快捷方式
    lnk_args = run_args.get(argsdef.ARG_KEY_LNK)
    if lnk_args or lnk_args == []:
        lnk_path = None if lnk_args == [] else lnk_args[0]
        args = ' '.join(lnk_args[1:])
        utils.create_shortcut(app_fullpath, lnk_path, args)
    # 程序没指定运行参数，进入WEBUI
    run_type = run_args.get(argsdef.ARG_KEY_RUN)
    if not run_type:
        if run_args.get(argsdef.ARG_KEY_ENV) == argsdef.ARG_ENV_TYPE_PROD:
            run_webui()
        else:
            webapp.run_app()
    else:
        # 首先确定运行日志记录方式
        log_type = run_args.get(argsdef.ARG_KEY_LOG)
        if log_type == argsdef.ARG_LOG_TYPE_FILE:  # 文件
            logger.use_file_logger()
            log_type = argsdef.ARG_LOG_TYPE_FILE
        elif log_type == argsdef.ARG_LOG_TYPE_CONSOLE:  # 控制台
            logger.use_console_logger()
            log_type = argsdef.ARG_LOG_TYPE_CONSOLE
        elif log_type == argsdef.ARG_LOG_TYPE_NONE:  # 禁用
            logger.user_none()
            log_type = argsdef.ARG_LOG_TYPE_NONE
        else:  # 文件和控制台
            logger.use_file_console_logger()
            log_type = argsdef.ARG_LOG_TYPE_BOTH
        # 最后确定程序运行方式
        if run_type == argsdef.ARG_RUN_TYPE_BACKGROUND:  # 后台
            run_in_the_background(log_type)
        elif run_type == argsdef.ARG_RUN_TYPE_POWERBOOT:  # 开机自启，后台
            run_on_startup(log_type)
        elif run_type == argsdef.ARG_RUN_TYPE_WEBUI:  # 启动WEBUI
            webapp.run_app()
        else:  # 控制台
            run_in_the_console()


if __name__ == '__main__':
    main()
