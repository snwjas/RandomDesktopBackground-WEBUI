# -*-coding:utf-8-*-
import imghdr
import json
import os
import random
import shutil
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures._base import Future
from typing import Dict, List

import requests

import configurator as configr
import const_config as const
import utils
from component import CustomLogger, SingletonMetaclass
from vo import ConfigVO, E

log = CustomLogger().get_logger()


class GetBackgroundTask(object, metaclass=SingletonMetaclass):
    from set_background import SetBackgroundTask

    """
    获取随机壁纸

    @author Myles Yang
    """

    def __init__(self, config: Dict[str, ConfigVO]):
        # 下载的壁纸任务
        # 总任务数量
        self.taskCount: int = 0
        # 已完成的任务数量（不论成功失败）
        self.taskDoneCount: int = 0
        # 已完成且成功的任务数量
        self.taskDoneSucceedCount: int = 0

        # 下载任务开始前，保存旧数据，任务完成后删除
        self.old_bg_abspaths: List[str] = []

        # 本次拉取下载的图片URL
        self.await_dwn_bg_urls: List[str] = []

        # 任务模式为一张时使用，记录当前已拉取到的下标，self.get_random_bg_urls()[self.single_curidx]
        self.single_curidx: int = 0
        # 任务模式：一张，是否在下载中
        self.single_dwning: bool = False

        self.is_getting_bg_urls: bool = False

        self.config: Dict[str, ConfigVO] = config
        self.sb_task: GetBackgroundTask.SetBackgroundTask = None

    def init_task(self, task: SetBackgroundTask):
        """
        初始化设置壁纸任务对象
        """
        self.sb_task = task

    def run(self):
        """
        拉取壁纸
        :return
        """
        if not self.sb_task:
            raise AttributeError("SetBackgroundTask对象未初始化，请执行init_task方法")

        if self.is_getting_bg_urls:
            return

        task_mode = configr.get_task_mode(self.config)
        if task_mode == const.Key.Task._MODE_MULTIPLE.value and self.taskCount > 0 \
                or task_mode == const.Key.Task._MODE_SINGLE.value and self.single_dwning:
            # log.info('后台正在拉取壁纸...请等待任务完成在执行此操作！')
            # utils.create_dialog('后台正在拉取壁纸...\n\n请等待任务完成在执行此操作!', const.dialog_title,
            #                     interval=2, style=win32con.MB_ICONWARNING)
            return

        # 保存原来的壁纸的路径
        self.old_bg_abspaths = configr.get_bg_abspaths()
        # 拉取壁纸
        self.auto_dwn_bg()

    def get_random_bg_urls(self) -> List[str]:
        """ 根据图源类型获取对应随机壁纸链接列表 """
        proxies = configr.get_proxies()
        if proxies:
            log.info('使用代理服务器配置拉取壁纸: {}'.format(proxies))
        api_name = configr.get_api_name(self.config)
        if api_name == const.Key.Api._NAME_WALLHAVEN.value:
            return self.__get_wallhaven_bg_urls(proxies)
        return self.__get_custom_bg_urls(proxies)

    def __get_wallhaven_bg_urls(self, proxies=None) -> List[str]:
        """ 获取wallhaven随机壁纸链接列表 """
        params = utils.get_request_params(configr.get_wallhaven_url(self.config))
        apikey = configr.get_wallhaven_apikey(self.config)
        if apikey:
            params['apikey'] = apikey
        if params.get('sorting') is None: params['sorting'] = 'random'
        bg_url_list = []
        resp = None
        try:
            # 如果排序未非随机，则附带随机页码参数
            if params.get('sorting') != 'random':
                params['page'] = 1
                resp = requests.get(const.wallhaven_api, params, headers=const.headers, proxies=proxies,
                                    timeout=(5, 60))
                if resp and resp.status_code == 200:
                    try:
                        data = json.loads(resp.text)
                        last_page = data.get('meta').get('last_page')
                        params['page'] = random.randint(1, int(last_page))
                    except:
                        params['page'] = 1
                time.sleep(1)
            resp = requests.get(const.wallhaven_api, params, headers=const.headers, proxies=proxies, timeout=(5, 60))
        except Exception as e:
            log.error('获取Wallhaven壁纸链接列表超时: {}'.format(e))

        if resp and resp.status_code == 200:
            try:
                data = json.loads(resp.text)
                for item in data.get('data'):
                    bg_url = item.get('path')
                    if bg_url:
                        bg_url_list.append(bg_url)
            except Exception as e:
                log.error('Wallhaven JSON数据解析错误: {}'.format(e))

        if resp and resp.status_code != 200:
            log.error("获取Wallhaven壁纸链接列表失败，状态码: {}，URL: {}，错误: {}".format(resp.status_code, resp.url, resp.text))

        return bg_url_list

    def __get_custom_bg_urls(self, proxies=None) -> List[str]:
        """ 获取自定义图源随机壁纸链接列表 """
        num = 24  # 链接数量，与wallhaven保持一致
        bg_url_list = []
        custom_urls = configr.get_custom_urls(self.config)
        if custom_urls:
            while num > 0:
                idx = random.randint(0, len(custom_urls) - 1)
                bg_url_list.append(custom_urls[idx])
                num -= 1
            return bg_url_list
        return self.__get_wallhaven_bg_urls(proxies)

    def auto_retain_bgs(self):
        bg_srcpath = configr.get_wallpaper_abspath(self.config)

        is_retain_bgs = configr.is_retain_bg_files(self.config)
        max_retain_mb = configr.get_max_retain_bg_mb(self.config)
        if is_retain_bgs and max_retain_mb != 0:
            # 保留壁纸
            dirname = time.strftime("retain-%Y%m%d", time.localtime())
            dir_path = os.path.join(bg_srcpath, dirname)
            os.makedirs(dir_path, exist_ok=True)
            for path in self.old_bg_abspaths:
                if os.path.isfile(path):
                    try:
                        shutil.move(path, dir_path)
                    except:
                        pass
            # 超出最大占用空间的进行删除
            if max_retain_mb != -1:  # -1无限制
                allow_size = max_retain_mb * 1024 * 1024
                # 1、获取已经保存的总大小
                bg_path_size = utils.get_path_size(bg_srcpath)
                # 2、进行删除，删除时间旧的（简单粗暴：直接删除一天）
                cur_size = bg_path_size
                if bg_path_size > allow_size:
                    # 获取已保存文件夹
                    dirs = list(filter(lambda p: os.path.isdir(os.path.join(bg_srcpath, p)), os.listdir(bg_srcpath)))
                    dirs.sort()
                    for p in dirs:
                        path = os.path.join(bg_srcpath, p)
                        size = utils.get_path_size(path)
                        succeed = utils.rm_file_dir(path)
                        if succeed:
                            cur_size -= size
                        if cur_size <= allow_size:
                            break
        else:  # 删除
            for path in self.old_bg_abspaths:
                if os.path.isfile(path):
                    try:
                        os.remove(path)
                    except:
                        pass
        self.old_bg_abspaths = []

    def __dwn_bg(self, bg_url: str, filename: str = None) -> str:
        """
        下载单个壁纸到 “const.bg_srcpath” 目录中
        :param bg_url: 壁纸链接
        :param filename: 壁纸文件名
        :return: 下载成功返回壁纸保存的绝对位置，否则为None
        """
        res_bg_abspath = None
        try:
            resp = requests.get(bg_url, headers=const.headers, proxies=configr.get_proxies(), timeout=(5, 120))
            if resp.status_code == 200:
                bg_srcpath = configr.get_wallpaper_abspath(self.config)
                os.makedirs(bg_srcpath, exist_ok=True)
                filename = filename if filename else "{}-{}".format(int(time.time() * 1000), os.path.basename(bg_url))
                bg_abspath = os.path.abspath(os.path.join(bg_srcpath, utils.get_win_valid_filename(filename)))
                with open(bg_abspath, 'wb') as bgfile:
                    bgfile.write(resp.content)
                res_bg_abspath = bg_abspath
            else:
                log.error("下载壁纸失败，状态码: {}，URL: {}，错误:\n {}".format(resp.status_code, resp.url, resp.text))
        except Exception as e:
            exc = E().e(e)
            log.error("下载壁纸失败: 原因：{}，URL:{}，错误：\n{}".format(exc.message, bg_url, exc.cause))
            return res_bg_abspath

        # 检测壁纸是否可用
        if utils.is_background_valid(res_bg_abspath):
            log.info('壁纸[{}]下载成功，URL：{}'.format(filename, bg_url))
            # 补全后缀
            fn, fe = os.path.splitext(filename)
            if not fe:
                try:
                    ext = imghdr.what(res_bg_abspath)
                    if ext:
                        new_res_bg_abspath = res_bg_abspath + '.' + ext
                        shutil.move(res_bg_abspath, new_res_bg_abspath)
                        res_bg_abspath = new_res_bg_abspath
                except:
                    pass
        else:
            try:
                os.remove(res_bg_abspath)
            except:
                pass
            res_bg_abspath = None

        return res_bg_abspath

    def __single_dwn_bg(self, bg_url):
        """ 单线程下载壁纸：（任务模式：一张） """
        self.single_dwning = True
        try:
            bg_abspath = self.__dwn_bg(bg_url)
            if bg_abspath:
                self.sb_task.set_bg_paths([])
                self.sb_task.add_bg_path(bg_abspath)
                self.sb_task.set_background_idx(0)
                self.auto_retain_bgs()
        finally:
            self.single_curidx += 1
            self.single_dwning = False

    def __parallel_dwn_bg(self, bg_urls):
        """
        多线程下载壁纸：（任务模式：多张）
        对于限流的网站，降低线程数，增加下载图片前的延时，以提高下载成功率
        :param bg_urls: 壁纸链接列表
        """
        self.taskCount = len(bg_urls)

        def dwn(bg_url: str, filename: str = None) -> str:
            rndsleep = configr.get_random_sleep(self.config)
            time.sleep(random.uniform(rndsleep[0], rndsleep[1]))
            return self.__dwn_bg(bg_url, filename)

        log.info('正在使用多线程拉取新的随机壁纸...')
        log.info('线程数量: {}，下载每个壁纸前随机暂停时间在{}之间'.format(
            configr.get_dwn_threads(self.config),
            configr.get_random_sleep(self.config)
        ))

        threads = configr.get_dwn_threads(self.config)
        with ThreadPoolExecutor(max_workers=threads, thread_name_prefix='DwnBg') as pool:
            for bg_url in bg_urls:
                future = pool.submit(dwn, bg_url)
                future.add_done_callback(self.__bg_parallel_dwned_callback)
            pool.shutdown(wait=True)

    def __bg_parallel_dwned_callback(self, future: Future):
        """
        重要函数，图片多线程下载完毕时的回调函数
        :param future: concurrent.futures._base.Future()
        """
        self.taskDoneCount += 1

        bg_abspath = str(future.result())
        if bg_abspath != str(None):
            self.taskDoneSucceedCount += 1
            self.sb_task.add_bg_path(bg_abspath)
            # 下载完成一张图片马上更新桌面背景
            if self.taskDoneSucceedCount == 1:
                self.sb_task.set_bg_paths([])
                self.sb_task.add_bg_path(bg_abspath)
                self.sb_task.set_background_idx(0)

        # 任务完成
        if self.taskDoneCount >= self.taskCount:
            log.info('壁纸拉取完毕，任务总数{}，成功{}'.format(self.taskCount, self.taskDoneSucceedCount))
            if self.taskDoneSucceedCount > 0:
                self.auto_retain_bgs()
            # 重置任务计数
            self.taskCount = self.taskDoneCount = self.taskDoneSucceedCount = 0

    def auto_dwn_bg(self):
        """ 拉取新壁纸，任务模式：一张 / 多张 """
        if self.is_getting_bg_urls: return
        self.is_getting_bg_urls = True
        try:
            task_mode = configr.get_task_mode(self.config)
            if task_mode == const.Key.Task._MODE_SINGLE.value:  # 每次下载一张
                if self.single_curidx >= len(self.await_dwn_bg_urls) - 1:
                    bg_urls = self.await_dwn_bg_urls = self.get_random_bg_urls()
                    self.single_curidx = 0
                    if bg_urls:
                        threading.Thread(
                            target=lambda: self.__single_dwn_bg(self.await_dwn_bg_urls[self.single_curidx])).start()
            else:  # 每次下载多张
                bg_urls = self.await_dwn_bg_urls = self.get_random_bg_urls()
                if bg_urls:
                    threading.Thread(target=lambda: self.__parallel_dwn_bg(bg_urls)).start()
                else:
                    self.taskCount = 0
        finally:
            self.is_getting_bg_urls = False
