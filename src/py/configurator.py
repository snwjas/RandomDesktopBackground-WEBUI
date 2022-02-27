# -*-coding:utf-8-*-

"""
相关配置配置读写解析

@author Myles Yang
"""

import os
import urllib.request
from typing import Dict, List, Tuple

import const_config as const
import dao
import utils
from vo import ConfigVO


def get_bg_abspaths():
    """
    获取壁纸目录下的绝对路径列表

    不包括子目录

    :return: 壁纸绝对路径列表
    """
    bg_srcpath = get_wallpaper_abspath()
    bg_paths = []
    try:
        if os.path.exists(bg_srcpath) and os.path.isfile(bg_srcpath):
            os.remove(bg_srcpath)
            return bg_paths
        os.makedirs(bg_srcpath, exist_ok=True)

        for df in os.listdir(bg_srcpath):
            df_abspath = os.path.join(bg_srcpath, df)
            if os.path.isfile(df_abspath):
                bg_paths.append(df_abspath)
    except:
        pass

    return bg_paths


def parse_config() -> Dict[str, ConfigVO]:
    """ 获取配置信息 """
    return dao.list_config()


"""============================ [Run] ============================"""


def get_workdir(config: Dict[str, ConfigVO] = None) -> str:
    """
    获取工作目录
    :return: 目录
    """
    key = const.Key.Run.WORKDIR.value
    vo = config.get(key) if config else dao.get_config(key)
    return vo.value if vo and vo.value else ''


def get_wallpaper_abspath(config: Dict[str, ConfigVO] = None) -> str:
    """ 壁纸保存目录 """
    workdir = get_workdir(config)
    workdir = workdir if workdir else 'run'
    return os.path.abspath(os.path.join(workdir, const.bg_srcpath))


def get_log_abspath(config: Dict[str, ConfigVO] = None) -> str:
    """ 运行日志保存目录 """
    workdir = get_workdir(config)
    workdir = workdir if workdir else 'run'
    return os.path.abspath(os.path.join(workdir, const.log_srcpath))


def get_favorite_abspath(config: Dict[str, ConfigVO] = None) -> str:
    """ 收藏文件夹 """
    workdir = get_workdir(config)
    workdir = workdir if workdir else 'run'
    return os.path.abspath(os.path.join(workdir, const.favorite_srcpath))


def get_proxies(config: Dict[str, ConfigVO] = None) -> Dict[str, str]:
    """ 获取用户代理
    :return: 代理配置
    """
    key = const.Key.Run.PROXY.value
    vo = config.get(key) if config else dao.get_config(key)
    proxy_name = vo.value if vo and vo.value else ''
    if proxy_name == const.Key.Run._PROXY_SYSTEM.value:
        return urllib.request.getproxies()
    return {}


def get_rotation(config: Dict[str, ConfigVO] = None) -> str:
    """ 获取轮播方式 """
    key = const.Key.Run.ROTATION.value
    vo = config.get(key) if config else dao.get_config(key)
    return vo.value if vo and vo.value else const.Key.Run._ROTATION_NETWORK.value


def is_local_disorder(config: Dict[str, ConfigVO] = None) -> bool:
    """ 是否为本地轮播且为无序 """
    key = const.Key.Run.LOCAL__DISORDER.value
    vo = config.get(key) if config else dao.get_config(key)
    rotation = get_rotation(config)
    return rotation == const.Key.Run._ROTATION_LOCAL.value and vo and vo.value


"""============================ [Api] ============================"""


def get_api_name(config: Dict[str, ConfigVO] = None) -> str:
    """ 获取API名字 """
    key = const.Key.Api.NAME.value
    vo = config.get(key) if config else dao.get_config(key)
    return vo.value if vo and vo.value else const.Key.Api._NAME_WALLHAVEN.value


def get_wallhaven_url(config: Dict[str, ConfigVO] = None) -> str:
    """ 获取 WALLHAVEN URL """
    key = const.Key.Api.WALLHAVEN__URL.value
    vo = config.get(key) if config else dao.get_config(key)
    return vo.value if vo and vo.value else vo.defaults


def get_wallhaven_apikey(config: Dict[str, ConfigVO] = None) -> str:
    """ 获取 WALLHAVEN API KEY """
    key = const.Key.Api.WALLHAVEN__APIKEY.value
    vo = config.get(key) if config else dao.get_config(key)
    return vo.value if vo and vo.value else ''


def get_custom_urls(config: Dict[str, ConfigVO] = None) -> List[str]:
    """ 获取自定义图源URL """
    key = const.Key.Api.CUSTOM.value
    config = config if config else dao.list_config(like_key='{}%'.format(key))
    result = []
    for k in config:
        if k and k.startswith(key):
            vo = config.get(k)
            if vo and vo.value:
                result.append(vo.value)
    return result


"""============================ [Task] ============================"""


def get_current(config: Dict[str, ConfigVO] = None) -> int:
    """
    获取配置中当前壁纸数组的下标
    :return: 值不存在或小于0，返回0
    """
    key = const.Key.Task.CURRENT.value
    vo = config.get(key) if config else dao.get_config(key)
    return vo.value if vo and vo.value else 0


def set_current(current: int = 0) -> int:
    """
    更新配置文件中当前壁纸数组的下标
    """
    vo = ConfigVO(const.Key.Task.CURRENT.value, current)
    return dao.update_config([vo], True)


def get_seconds(config: Dict[str, ConfigVO] = None) -> int:
    """
    获取桌面背景更换的频率
    :return: 值不存在或小于10，返回300
    """
    key = const.Key.Task.SECONDS.value
    vo = config.get(key) if config else dao.get_config(key)
    return vo.value if vo and vo.value else 600


def get_task_mode(config: Dict[str, ConfigVO] = None) -> str:
    """ 获取任务模式：多张 / 一张 """
    key = const.Key.Task.MODE.value
    vo = config.get(key) if config else dao.get_config(key)
    return vo.value if vo and vo.value else const.Key.Task._MODE_MULTIPLE.value


def get_dwn_threads(config: Dict[str, ConfigVO] = None) -> int:
    """
    获取下载壁纸时的线程数
    """
    key = const.Key.Task.THREADS.value
    vo = config.get(key) if config else dao.get_config(key)
    return vo.value if vo and vo.value else min(32, (os.cpu_count() or 1) + 4)


def get_random_sleep(config: Dict[str, ConfigVO] = None) -> Tuple[float, float]:
    """
    获取在下载壁纸前的随机睡眠时间
    :return tuple: 返回两个元素的元组，生成两个数间的随机值
    """
    l_key = const.Key.Task.RND_SLEEP_L.value
    r_key = const.Key.Task.RND_SLEEP_R.value
    L = config.get(l_key) if config else dao.get_config(l_key)
    R = config.get(r_key) if config else dao.get_config(r_key)

    lval = L.value if L and L.value else 0.5
    rval = R.value if R and R.value else 5

    # 判断两个值大小是否反了
    if lval > rval:
        tmp = rval
        rval = lval
        lval = tmp

    return lval, rval


def is_retain_bg_files(config: Dict[str, ConfigVO] = None) -> bool:
    """
    在拉取新的壁纸前，是否保留旧的壁纸
    """
    key = const.Key.Task.RETAIN_BGS.value
    vo = config.get(key) if config else dao.get_config(key)
    return vo and vo.value


def get_max_retain_bg_mb(config: Dict[str, ConfigVO] = None) -> int:
    """
    获取壁纸保留最大占用存储空间
    """
    key = const.Key.Task.MAX_RETAIN_MB.value
    vo = config.get(key) if config else dao.get_config(key)
    return vo.value if vo and vo.value else 0


"""============================ [Hotkey] ============================"""


def is_hotkey_enabled(config: Dict[str, ConfigVO] = None) -> bool:
    """
    是否启用热键
    """
    key = const.Key.Hotkey.ENABLE.value
    vo = config.get(key) if config else dao.get_config(key)
    return vo and vo.value


def get_hotkey_prev(config: Dict[str, ConfigVO] = None) -> List[str]:
    """
    获取热键：上一个壁纸
    """
    key = const.Key.Hotkey.PREV_BG.value
    vo = config.get(key) if config else dao.get_config(key)
    return __get_hotkey(vo)


def get_hotkey_next(config: Dict[str, ConfigVO] = None) -> List[str]:
    """
    获取热键：下一个壁纸
    """
    key = const.Key.Hotkey.NEXT_BG.value
    vo = config.get(key) if config else dao.get_config(key)
    return __get_hotkey(vo)


def get_hotkey_favorite(config: Dict[str, ConfigVO] = None) -> List[str]:
    """
    获取热键：收藏当前壁纸
    """
    key = const.Key.Hotkey.FAV_BG.value
    vo = config.get(key) if config else dao.get_config(key)
    return __get_hotkey(vo)


def get_hotkey_locate(config: Dict[str, ConfigVO] = None) -> List[str]:
    """
    获取热键：定位到当前壁纸
    """
    key = const.Key.Hotkey.LOC_BG.value
    vo = config.get(key) if config else dao.get_config(key)
    return __get_hotkey(vo)


def __get_hotkey(config: ConfigVO) -> List[str]:
    """
    获取热键通用方法
    """
    if not config or not config.value:
        return []
    hk = utils.get_split_value(config.value, '+', opt_type=str)
    return utils.list_deduplication(hk)


"""============================ PID ============================"""


def record_pid(ptype: str, running: bool = True) -> int:
    """
    记录程序运行的PID
    """
    pid = os.getpid() if running else -1
    if ptype == 'bpid':
        i = dao.update_config([ConfigVO(const.Key.Run.BPID.value, pid)], True)
    elif ptype == 'fpid':
        i = dao.update_config([ConfigVO(const.Key.Run.FPID.value, pid)], True)
    return pid


def record_bpid(running: bool = True) -> int:
    return record_pid('bpid', running)


def record_fpid(running: bool = True) -> int:
    return record_pid('fpid', running)


def get_pid(ptype: str) -> int:
    """
    获取PID
    :param ptype: bpid | fpid
    :return int: 返回PID，获取失败返回-1
    """
    if ptype == 'bpid':
        config = dao.get_config(const.Key.Run.BPID.value)
    elif ptype == 'fpid':
        config = dao.get_config(const.Key.Run.FPID.value)
    else:
        return -1

    if config and config.value:
        return int(config.value)
    else:
        return -1


def get_bpid() -> int:
    """ 获取后台运行程序ID """
    return get_pid('bpid')


def get_fpid() -> int:
    """ 获取前台运行程序ID（webui服务） """
    return get_pid('fpid')
