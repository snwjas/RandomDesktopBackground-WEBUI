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
from component import CustomLogger, SimpleMmapActuator
from get_background import GetBackgroundTask
from set_background import SetBackgroundTask
from vo import E

app_fullpath = os.path.abspath(sys.argv[0])
app_dirname = os.path.dirname(app_fullpath)

logger = CustomLogger()
log = logger.get_logger()


def run_in_the_background():
    # 检测程序是否在运行
    arg_dict = argsdef.arg_dict
    run_type = arg_dict.get(argsdef.ARG_KEY_RUN)
    if run_type and run_type != argsdef.ARG_RUN_TYPE_WEBUI:
        if utils.is_process_running(configr.get_bpid(), app_fullpath):
            utils.create_dialog("检测到程序在运行中，请勿重复启动！", const.dialog_title,
                                style=win32con.MB_ICONERROR, interval=5)
            return

    log.info('程序启动，当前系统操作系统: {}-{}'.format(platform.platform(), platform.architecture()))
    try:

        config = configr.parse_config()

        gtask = GetBackgroundTask(config)
        stask = SetBackgroundTask(config, gtask.run)

        gtask.init_task(stask)

        stask.run()

        # 记录运行中程序的PID
        configr.record_bpid()
    except Exception as e:
        exc = E().e(e)
        log.error("程序启动错误：{}\n{}".format(exc.message, exc.cause))


def run_on_startup():
    """
    开机时启动，默认以后台方式运行程序
    """
    # 创建快捷方式到用户开机启动目录: shell:startup
    from service import create_startup_lnk
    create_startup_lnk()
    # 后台运行
    return run_in_the_background()


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
    return True


def main():
    if not check():
        return

    # 获取启动参数
    run_args = argsdef.arg_dict
    # 程序没指定运行参数，进入WEBUI
    run_type = run_args.get(argsdef.ARG_KEY_RUN)
    if not run_type:
        webapp.run_app()
    else:
        # 初始化logger
        logger.set_logpath(configr.get_log_abspath())
        # 首先确定运行日志记录方式
        log_type = run_args.get(argsdef.ARG_KEY_LOG)
        if log_type == argsdef.ARG_LOG_TYPE_FILE:  # 文件
            logger.use_file_logger()
        elif log_type == argsdef.ARG_LOG_TYPE_CONSOLE:  # 控制台
            logger.use_console_logger()
        elif log_type == argsdef.ARG_LOG_TYPE_NONE:  # 禁用
            logger.user_none()
        # 最后确定程序运行方式
        if run_type == argsdef.ARG_RUN_TYPE_CONSOLE:  # 控制台
            pass
        elif run_type == argsdef.ARG_RUN_TYPE_BACKGROUND:  # 后台
            if not log_type: logger.use_file_logger()
            run_in_the_background()
        elif run_type == argsdef.ARG_RUN_TYPE_POWERBOOT:  # 开机自启，后台
            if not log_type: logger.use_file_logger()
            run_on_startup()
        elif run_type == argsdef.ARG_RUN_TYPE_WEBUI:  # 启动WEBUI
            webapp.run_app()
        elif run_type == argsdef.ARG_RUN_TYPE_LNK:  # 创建程序快捷方式
            lnk_args = run_args.get(argsdef.ARG_KEY_LNK)
            if lnk_args or lnk_args == []:
                lnk_path = None if lnk_args == [] else lnk_args[0]
                args = ' '.join(lnk_args[1:])
                utils.create_shortcut(app_fullpath, lnk_path, args)
        elif run_type == argsdef.ARG_RUN_TYPE_CMD:  # 执行定义命令
            cmd = run_args.get(argsdef.ARG_KEY_CMD)
            if cmd in argsdef.CHOICES_ARG_CMD_TYPE:
                sma = SimpleMmapActuator()
                sma.send_command(cmd)


if __name__ == '__main__':
    main()
