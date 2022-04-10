# -*-coding:utf-8-*-

"""
程序启动参数定义、获取与解析

@author Myles Yang
"""

import argparse

import const_config as const

""" 设置命令参数时的KEY """
# 程序运行方式
ARG_KEY_RUN = ARG_RUN = '--run'
# 程序日志记录方式
ARG_KEY_LOG = ARG_LOG = '--log'
# 创建程序快捷方式
ARG_KEY_LNK = ARG_LNK = '--lnk'
# 启动环境
ARG_KEY_ENV = ARG_ENV = '--env'
# 运行中可执行指令
ARG_KEY_CMD = ARG_CMD = '--cmd'

""" --run 命令参数选项 """
# 控制台启动
ARG_RUN_TYPE_CONSOLE = 'console'
# 控制台后台启动
ARG_RUN_TYPE_BACKGROUND = 'background'
# 开机自启，控制台后台启动
ARG_RUN_TYPE_POWERBOOT = 'powerboot'
# 启动WEBUI
ARG_RUN_TYPE_WEBUI = 'webui'
# 创建快捷方式
ARG_RUN_TYPE_LNK = 'lnk'
# 发送执行命令
ARG_RUN_TYPE_CMD = 'cmd'
# 选择项
CHOICES_ARG_RUN_TYPE = [ARG_RUN_TYPE_CONSOLE, ARG_RUN_TYPE_BACKGROUND, ARG_RUN_TYPE_POWERBOOT,
                        ARG_RUN_TYPE_WEBUI, ARG_RUN_TYPE_LNK, ARG_RUN_TYPE_CMD]

""" --log 命令参数选项 """
# 控制台打印方式记录运行日志
ARG_LOG_TYPE_CONSOLE = 'console'
# 文件方式记录运行日志
ARG_LOG_TYPE_FILE = 'file'
# 文件和控制台打印方式记录运行日志
ARG_LOG_TYPE_BOTH = 'both'
# 禁用日志记录
ARG_LOG_TYPE_NONE = 'none'
# 选择项
CHOICES_ARG_LOG_TYPE = [ARG_LOG_TYPE_CONSOLE, ARG_LOG_TYPE_FILE, ARG_LOG_TYPE_BOTH, ARG_LOG_TYPE_NONE]

""" --env 命令参数选项 """
# 生产环境
ARG_ENV_TYPE_PROD = 'prod'
# 开发环境
ARG_ENV_TYPE_DEV = 'dev'
# 选择项
CHOICES_ARG_ENV_TYPE = [ARG_ENV_TYPE_PROD, ARG_ENV_TYPE_DEV]

""" --cmd 命令参数选项 """
# 下一张壁纸
ARG_CMD_TYPE_NXT = 'nxt'
# 上一张壁纸
ARG_CMD_TYPE_PRE = 'pre'
# 收藏当前壁纸
ARG_CMD_TYPE_FAV = 'fav'
# 定位当前壁纸
ARG_CMD_TYPE_LOC = 'loc'
# 选择项
CHOICES_ARG_CMD_TYPE = [ARG_CMD_TYPE_NXT, ARG_CMD_TYPE_PRE, ARG_CMD_TYPE_FAV, ARG_CMD_TYPE_LOC]

"""
定义命令行输入参数
"""
parser = argparse.ArgumentParser(
    prog=const.app_name,
    description='{}命令行参数'.format(const.app_name),
)

parser.add_argument('-r', ARG_RUN,
                    help='指定程序的运行方式',
                    type=str,
                    choices=CHOICES_ARG_RUN_TYPE,
                    dest=ARG_KEY_RUN
                    )

parser.add_argument('-l', ARG_LOG,
                    help='指定运行日志记录方式',
                    type=str,
                    choices=CHOICES_ARG_LOG_TYPE,
                    dest=ARG_KEY_LOG
                    )

parser.add_argument('-e', ARG_ENV,
                    help='指定程序的运行环境',
                    type=str,
                    choices=CHOICES_ARG_ENV_TYPE,
                    dest=ARG_KEY_ENV,
                    default=ARG_ENV_TYPE_PROD
                    )

parser.add_argument('-s', ARG_LNK,
                    help='根据给的路径创建程序的快捷方式，与--run组合使用',
                    type=str,
                    nargs='*',
                    dest=ARG_KEY_LNK
                    )

parser.add_argument('-c', ARG_CMD,
                    help='运行中可执行指令，与--run组合使用',
                    type=str,
                    choices=CHOICES_ARG_CMD_TYPE,
                    dest=ARG_KEY_CMD
                    )

arg_dict = vars(parser.parse_args())
