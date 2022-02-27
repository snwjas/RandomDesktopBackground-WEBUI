# -*-coding:utf-8-*-
import ctypes
import os
import random
import shutil
import time
from threading import Thread
from typing import Dict, Callable, List

import win32con
import win32gui
from system_hotkey import SystemHotkey

import configurator as configr
import const_config as const
import utils
from component import CustomLogger, SingletonMetaclass
from component import SimpleTaskTimer
from utils import is_background_valid
from vo import ConfigVO, E

user32 = ctypes.windll.user32

log = CustomLogger().get_logger()

# 允许的使用快捷键时进行切换的间隔时间
_allowed_manual_switching_interval_time = 0.562632


class SetBackgroundTask(object, metaclass=SingletonMetaclass):
    """
    切换桌面背景后台任务

    @author Myles Yang
    """

    def __init__(self, config: Dict[str, ConfigVO], get_bg_func: Callable):
        """
        :param config: 配置
        :param get_bg_func: 拉取壁纸的函数
        """
        self.__config = config
        self.__bg_paths = configr.get_bg_abspaths()
        self.__current = self.set_current(configr.get_current(config))
        self.__seconds = configr.get_seconds(config)

        self.__func_get_bg = get_bg_func
        if not (get_bg_func or callable(get_bg_func)):
            raise AttributeError("请正确传入拉取壁纸的函数形参get_bg_func")

        # 记录上一次切换壁纸的时间，防止频繁切换
        self.__last_change_time = time.time() - 1314.71861

        self.__timer: SimpleTaskTimer = None
        self.__hotkey: SystemHotkey = None

    def get__bg_paths(self):
        """
        bg_paths getter
        """
        return self.__bg_paths

    def set_bg_paths(self, bg_paths: list):
        """
        bg_paths setter
        """
        self.__bg_paths = bg_paths

    def add_bg_path(self, bg_path: str):
        """
        add to bg_paths
        :param bg_path: 壁纸绝对路径
        """
        self.__bg_paths.append(bg_path)

    def get_current(self):
        """
        current getter
        """
        return self.__current

    def set_current(self, current: int):
        """
        current setter
        """
        current = current if 0 <= current < len(self.__bg_paths) else 0
        self.__current = current
        configr.set_current(current)
        return current

    def run(self):
        """
        启动切换桌面背景后台任务
        """
        if self.__timer and self.__timer.is_running():
            log.info('自动切换随机桌面背景后台任务已启动，无需再启动')
            return

        log.info('自动切换随机桌面背景任务已启动')
        log.info('桌面背景切换间隔：{}秒'.format(self.__seconds))

        # 绑定全局热键
        self.bind_hotkey()
        # 开启后台定时切换任务
        self.__timer = SimpleTaskTimer()
        self.__timer.run(self.__seconds, self.next_bg)

        # 切换当前壁纸
        if self.__bg_paths:
            if 0 <= self.__current < len(self.__bg_paths):
                self.set_background(self.__bg_paths[self.__current])
            else:
                self.set_background_idx(0)
        else:
            self.set_current(0)
            self.next_bg()

    def next_bg(self):
        """
        切换下一个壁纸
        """

        # 锁屏状态下不切换
        if utils.is_lock_workstation():
            return

        if configr.is_local_disorder(self.__config):
            self.random_bg()
            return

        # 限制热键切换频率
        if time.time() - self.__last_change_time < _allowed_manual_switching_interval_time:
            return

        # 重新拉取图片
        if (not self.__bg_paths) or self.__current >= len(self.__bg_paths) - 1:
            self.__get_backgrounds()
            return
        nxt = self.__current + 1
        while nxt < len(self.__bg_paths):
            set_res = self.set_background(self.__bg_paths[nxt], nxt)
            if set_res:
                self.set_current(nxt)
                return
            nxt += 1
        if nxt >= len(self.__bg_paths) - 1:
            self.__get_backgrounds()

    def prev_bg(self):
        """
        切换上一个壁纸
        """
        if configr.is_local_disorder(self.__config):
            self.random_bg()
            return

        if time.time() - self.__last_change_time < _allowed_manual_switching_interval_time:
            return

        if (not self.__bg_paths) or self.__current <= 0:
            utils.create_dialog("已是第一个桌面背景了，不能再切换上一个", const.dialog_title,
                                interval=2, style=win32con.MB_ICONWARNING)
            return
        pre = self.__current - 1
        while pre >= 0:
            set_res = self.set_background(self.__bg_paths[pre], pre)
            if set_res:
                self.set_current(pre)
                return
            pre -= 1

    def random_bg(self):
        """ 随机切换壁纸 """
        if not self.__bg_paths:
            return
        idx = random.randint(0, len(self.__bg_paths) - 1)
        self.set_background_idx(idx)

    def locate_bg(self):
        """
        在资源管理器定位当前桌面背景文件
        """
        if self.__bg_paths:
            utils.locate_path(self.__bg_paths[self.__current])

    def favorite_bg(self):
        """
        收藏当前壁纸至收藏目录
        """
        if self.__bg_paths:
            favorite_srcpath = configr.get_favorite_abspath(self.__config)
            os.makedirs(favorite_srcpath, exist_ok=True)
            try:
                shutil.copy(self.__bg_paths[self.__current], favorite_srcpath)
                utils.create_dialog('已收藏壁纸[{}]至收藏目录'.format(os.path.basename(self.__bg_paths[self.__current])),
                                    const.dialog_title, style=win32con.MB_ICONINFORMATION, interval=2)
            except:
                pass

    def __get_backgrounds(self):
        """
        重新拉取壁纸
        """
        if configr.get_rotation(self.__config) == const.Key.Run._ROTATION_LOCAL.value:
            """ 本地顺序轮询 """
            self.set_background_idx(0)
            return
        if not utils.is_network_available():
            log.info('网络不连通，取消拉取壁纸，重新轮换已下载的壁纸')
            self.set_background_idx(0)
            return
        # self.__func_get_bg()
        Thread(target=self.__func_get_bg).start()

    def set_background(self, abs_path: str, index: int = None):
        """
        设置桌面背景，使用windows api

        如果路径无效，也会生成一张纯色的图片，设置的壁纸会临时存放在路径
        "%USERPROFILE%/AppData/Roaming/Microsoft/Windows/Themes/CachedFiles"

        :param abs_path: 壁纸绝对路径
        :param index: 当前壁纸列表下标
        :return: True-设置成功; False-设置失败
        """
        if is_background_valid(abs_path):
            try:
                # 在32位win7中测试，频繁切换会报错，故限制了切换频率
                # 设置桌面背景，最后一个参数：SPIF_UPDATEINIFILE(在原路径设置)，win32con.SPIF_SENDWININICHANGE（复制图片到缓存）
                win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, abs_path, win32con.SPIF_SENDWININICHANGE)
                self.__last_change_time = time.time()
            except:
                return False
            cur_bg = index + 1 if (index or index == 0) else self.__current + 1
            log.info('切换桌面背景，总数{}，当前{}'.format(len(self.__bg_paths), cur_bg))
            return True
        return False

    def set_background_idx(self, index: int):
        """ 设置壁纸 """
        if self.__bg_paths and 0 <= index < len(self.__bg_paths):
            self.set_current(index)
            return self.set_background(self.__bg_paths[index])
        return False

    def __get_hotkey_cb(self, data: dict):
        def callback():
            try:
                log.info('执行热键[{}]:{}'.format(data.get('name'), data.get('hk')))
                data.get('cb')()
            except Exception as e:
                exc = E().e(e)
                log.error('热键[{}]事件[{}]执行错误:{}，原因:\n{}'.format(
                    data.get('hk'), data.get('name'), exc.message, exc.cause))

        return lambda p: callback()

    def bind_hotkey(self):
        """
        绑定热键
        """
        if self.__hotkey or not configr.is_hotkey_enabled(self.__config):
            return

        self.__hotkey = SystemHotkey(check_queue_interval=0.01)
        # 热键绑定的数量
        bind_count = 0
        # 热键绑定成功的数量
        bind_succeed_count = 0
        # 热键绑定失败提示消息
        bind_error_msg = ''

        hks_to_bind = [
            {
                'hk': configr.get_hotkey_prev(self.__config),
                'name': '上一个桌面背景',
                'cb': self.prev_bg
            },
            {
                'hk': configr.get_hotkey_next(self.__config),
                'name': '下一个桌面背景',
                'cb': self.next_bg
            },
            {
                'hk': configr.get_hotkey_locate(self.__config),
                'name': '定位当前桌面背景文件',
                'cb': self.locate_bg
            },
            {
                'hk': configr.get_hotkey_favorite(self.__config),
                'name': '收藏当前壁纸',
                'cb': self.favorite_bg
            }
        ]

        for hk_info in hks_to_bind:
            hk = hk_info.get('hk')
            hk_name = hk_info.get('name')
            if hk:
                bind_count += 1
                valid, msg = self.is_hotkey_valid(self.__hotkey, hk)
                if valid:
                    # system_hotkey 模块存在Bug，作者尚未修复
                    # 热键在子线程中注册，其中overwrite无论真假，当试图绑定了一个原有的热键时，会抛出错误，
                    # 但无法在主线程捕获，而且会造成绑定热键的队列阻塞？，进而造成所有热键失效。
                    try:
                        self.__hotkey.register(hk, callback=self.__get_hotkey_cb(hk_info), overwrite=True)
                    except Exception as e:
                        log.error('热键[{}]绑定失败，热键：{}，原因：{}'.format(hk_name, hk, e))
                        bind_error_msg += '热键[{}]绑定失败：{}\n'.format(hk_name, hk)
                        continue
                    bind_succeed_count += 1
                    log.info('热键[{}]绑定成功: {}'.format(hk_name, hk))
                else:
                    log.error('热键[{}]绑定失败，热键：{}，原因：{}'.format(hk_name, hk, msg))
                    bind_error_msg += '热键[{}]绑定失败：{}\n'.format(hk_name, hk)

        # 检测热键绑定情况
        if bind_succeed_count == 0:
            self.__hotkey = None
        elif bind_succeed_count < bind_count:
            # 设置非阻塞自动关闭对话框，防止阻塞线程
            utils.create_dialog(bind_error_msg, const.dialog_title, style=win32con.MB_ICONWARNING, interval=7)

    def unbind_hotkey(self):
        """
        解绑热键
        """
        pass

    def is_hotkey_valid(self, hkobj: SystemHotkey, hk: List[str]):
        """
        检测热键是否可用，因为 SystemHotkey 注册热键存在BUG，在注册前进行检测？
        """
        hk = hkobj.order_hotkey(hk)
        try:
            keycode, masks = hkobj.parse_hotkeylist(hk)
            reg_hk_res = user32.RegisterHotKey(None, 1, masks, keycode)
            # time.sleep(0.1)
            if reg_hk_res:
                user32.UnregisterHotKey(None, reg_hk_res)
            else:
                return False, '热键被占用'
        except Exception as e:
            return False, e

        return True, '热键可被注册'
