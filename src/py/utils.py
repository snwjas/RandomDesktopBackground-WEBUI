# -*-coding:utf-8-*-

"""
工具模块

@author Myles Yang
"""
import ctypes
import imghdr
import json
import os
import pickle
import re
import shutil
import threading
import time
import typing
import urllib.request
import webbrowser
from typing import List

import pythoncom
import requests
import win32api
import win32com.client as win32com_client
import win32con
import win32gui
import win32process
import win32ui
from requests import Response
from win32comext.shell import shell, shellcon

import const_config as const
from vo import E

user32 = ctypes.windll.user32


def is_background_valid(file) -> bool:
    """
    判断壁纸是否可用（是否是允许的图片类型）

    :param file: 壁纸绝对位置 / 壁纸的file对象
    :return: (可用，文件后缀)
    """
    try:
        # 这玩意有时正常格式图片会检测不出来
        file_ext = imghdr.what(file)
        # 图片后缀，这些基本够用了，实际在设置时windows会将图片转换为jpg格式
        # 这些后缀的图片经过测试都能设置为桌面背景
        valid_img_ext_patn = r'png|jp[e]{0,1}g|gif|bmp|tif'
        if file_ext and re.match(valid_img_ext_patn, file_ext):
            return True
    except:
        pass
    return False


def set_background(img_abs_path: str) -> bool:
    """
    windows设置桌面背景，最后一个参数：SPIF_UPDATEINIFILE(在原路径设置)，win32con.SPIF_SENDWININICHANGE（复制图片到缓存）
    如果路径无效，也会生成一张纯色的图片，设置的壁纸会临时存放在路径"%USERPROFILE%/AppData/Roaming/Microsoft/Windows/Themes/CachedFiles"
    """
    try:
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, img_abs_path, win32con.SPIF_SENDWININICHANGE)
        return True
    except:
        pass
    return False


def set_background_fit(wallpaper_style=0, tile_wallpaper=0):
    """
    设置桌面背景契合度（交给用户自行设置）
    """

    # 打开指定注册表路径
    sub_reg_path = "Control Panel\\Desktop"
    reg_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, sub_reg_path, 0, win32con.KEY_SET_VALUE)
    # WallpaperStyle:2拉伸,6适应,10填充,22跨区，其他0
    win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, str(wallpaper_style))
    # TileWallpaper：1平铺，居中0，其他0
    win32api.RegSetValueEx(reg_key, "TileWallpaper", 0, win32con.REG_SZ, str(tile_wallpaper))
    win32api.RegCloseKey(reg_key)


def get_shortcut(shortcut) -> str:
    """
    获取快捷方式
    :param shortcut: 快捷方式对象或路径
    :return: 快捷方式指向的文件绝对路径
    """
    if not is_main_thread():
        pythoncom.CoInitialize()
    try:
        ws = win32com_client.Dispatch("WScript.Shell")
        return ws.CreateShortCut(shortcut).Targetpath
    except Exception as e:
        raise E().e(e, message="获取快捷方式[{}]指向目标失败".format(shortcut))
    finally:
        if not is_main_thread():
            pythoncom.CoUninitialize()


def create_shortcut(filename: str, lnkname: str = None, args: str = None, style: int = None):
    """
    创建快捷方式
    :param filename: 目标文件名（需含路径）
    :param lnkname: 快捷方式名，可以是路径，也可以的包含路径的文件名（文件名需含后缀.lnk），
                    还可以是windows特殊路径，它必须以shell:开头，如shell:desktop表示桌面路径
    :param args: 启动程序的参数
    :param style: 窗口样式，1.Normal window普通窗口,3.Maximized最大化窗口,7.Minimized最小化
    :return: 快捷方式对象(快捷方式路径)
    """
    target_path = os.path.abspath(filename)

    def get_lnkname():
        fp, fn = os.path.split(target_path)
        mn, ext = os.path.splitext(fn)
        return mn + '.lnk'

    if not lnkname:
        lnkname = get_lnkname()
    else:
        if os.path.isdir(lnkname):
            lnkname = os.path.join(lnkname, get_lnkname())
        else:
            if lnkname.lower().startswith('shell:'):
                # shell:desktop:lnkName
                sarr = lnkname.split(':')
                spec_dir = get_special_folders(sarr[1])
                if spec_dir:
                    ln = get_lnkname()
                    if len(sarr) == 3:
                        ln = sarr[2] if sarr[2].lower().endswith('.lnk') else sarr[2] + '.lnk'
                    lnkname = os.path.join(spec_dir, ln)

    if not is_main_thread():
        pythoncom.CoInitialize()
    try:
        ws = win32com_client.Dispatch("WScript.Shell")
        shortcut = ws.CreateShortCut(lnkname)
        shortcut.TargetPath = target_path
        shortcut.WorkingDirectory = os.path.split(target_path)[0]
        shortcut.Arguments = args.strip() if args else ''
        shortcut.WindowStyle = style if (style and style in [1, 3, 7]) else 1
        shortcut.Save()
        return shortcut
    except Exception as e:
        raise E().e(e, message="创建程序[{}]快捷方式失败".format(target_path))
    finally:
        if not is_main_thread():
            pythoncom.CoUninitialize()


def get_special_folders(name: str) -> str:
    """
    获取 windows 特定目录路径
    :param name: windows目录特定值名称，如Desktop、Startup...
    """
    if not is_main_thread():
        pythoncom.CoInitialize()
    try:
        ws = win32com_client.Dispatch("WScript.Shell")
        return ws.SpecialFolders(name)
    except Exception as e:
        raise E().e(e, message="获取 windows 特定目录路径[{}]失败".format(name))
    finally:
        if not is_main_thread():
            pythoncom.CoUninitialize()


def locate_path(path: str, is_select: bool = True) -> None:
    """
    打开资源管理器定位到相应路径
    :param path: 目标路径
    :param is_select: true定位选择目标，false打开目录
    """
    if path and os.path.exists(path):
        os.popen('explorer /e,{} "{}"'.format(
            '/select,' if is_select else '',
            path
        ))


def run_in_background(executable_target: str, args: str = ''):
    """
     后台运行目标程序
    :param executable_target: 可执行目标路径
    :param args: 参数
    :return: (bool: 是否成功, str：结果消息)
    """
    if not is_main_thread():
        pythoncom.CoInitialize()
    try:
        ws = win32com_client.Dispatch("WScript.Shell")
        executable_cmd = '"{}"{}'.format(executable_target, args) if args else '"{}"'.format(executable_target)
        res = ws.Run(executable_cmd, 0)
        return True, res
    except Exception as e:
        return False, str(e)
    finally:
        if not is_main_thread():
            pythoncom.CoUninitialize()


def set_foreground_window(target, block: bool = True) -> None:
    """
    设置 windows 窗口处于前台

    :param target: 窗口句柄或窗口标题
    :param block: 是否阻塞执行
    :return:
    """
    if not target:
        return

    def f():
        times_retry = 10
        while times_retry > 0:
            time.sleep(0.1)
            hwnd = None
            if isinstance(target, str):
                hwnd = win32gui.FindWindow(None, target)
            if hwnd and isinstance(target, int):
                try:
                    win32gui.SetForegroundWindow(hwnd)
                finally:
                    return
            times_retry -= 1

    if block:
        f()
    else:
        threading.Thread(target=lambda: f()).start()


def create_dialog(message: str, title: str, style: int = win32con.MB_OK,
                  block: bool = None, interval: float = 0, callback=None):
    """
    使用微软未公布的Windows API: MessageBoxTimeout 实现自动关闭的对话框，通过user32.dll调用，
    相比于使用 MessageBox 来实现显得更加简洁，参数详情请参考以上函数 create_dialog

    调用时 style 请不要 与 上 MB_SETFOREGROUND

    值得注意的是 Windows 2000 没有导出该函数。并且对于多选一没有关闭/取消功能的对话框，
    自动关闭时默认(回调)返回值为 32000

    :param message: 对话框消息内容
    :param title: 对话框标题
    :param style: 对话框类型，该值可以相加组合出不同的效果。
    :param block: 对话框是否阻塞调用线程，默认值取决于interval<=0，为Ture不会自动关闭，意味着阻塞调用线程
    :param interval: 对话框自动关闭秒数
    :param callback: 对话框关闭时的回调函数，含一参数为对话框关闭结果(按下的按钮值)
    :return: 当对话框为非阻塞时，无返回值(None)，否则，对话框阻塞当前线程直到返回,值为按下的按钮值
    """

    block = block if (block is not None) else interval <= 0
    interval = int(interval * 1000) if interval > 0 else 0

    def show():
        # if UNICODE MessageBoxTimeoutW else MessageBoxTimeoutA
        # MessageBoxTimeout(hwnd, lpText, lpCaption, uType, wLanguageId, dwMilliseconds)
        btn_val = user32.MessageBoxTimeoutW(0, message, title, style | win32con.MB_SETFOREGROUND, 0, interval)
        if callback and callable(callback):
            callback(btn_val)
        return btn_val

    if block:
        return show()
    else:
        threading.Thread(target=show).start()


def list_deduplication(li: list) -> list:
    """
    列表去重
    """
    if not li:
        return list()
    res = list(set(li))
    res.sort(key=li.index)
    return res


def is_main_thread() -> bool:
    """
    检测当前线程是否为主线程
    """
    return threading.current_thread() is threading.main_thread()


def is_lock_workstation() -> bool:
    """
    判断Windows是否处于锁屏状态
    目前暂时无法做到检测屏幕关屏状态
    """
    hwnd = win32gui.GetForegroundWindow()
    return hwnd <= 0


def is_process_running(pid: int):
    """ 判断进程是否在运行
    :param pid: 进程ID
    """
    try:
        return win32process.GetProcessVersion(pid) > 0
    except:
        return False


def select_folder(msg: str = "选择文件夹") -> str:
    """
    选择文件夹
    :param msg: 描述信息
    :return: 选择的文件夹路径
    """
    """ SHBrowseForFolder:
            HWND hwndOwner;            // 父窗口句柄
            LPCITEMIDLIST pidlRoot;    // 要显示的文件目录对话框的根(Root)
            LPCTSTR lpszTitle;         // 显示位于对话框左上部的标题
            UINT ulFlags;              // 指定对话框的外观和功能的标志
            BFFCALLBACK lpfn;          // 处理事件的回调函数
            LPARAM lParam;             // 应用程序传给回调函数的参数
    """
    try:
        pidl, display_name, image_list = shell.SHBrowseForFolder(
            win32gui.GetForegroundWindow(),  # win32gui.GetDesktopWindow(),
            shell.SHGetFolderLocation(0, shellcon.CSIDL_DESKTOP, 0, 0),
            msg,
            shellcon.BIF_RETURNONLYFSDIRS | 0x00000040,
            None,
            None
        )
        if pidl is None:
            return None
        else:
            path = shell.SHGetPathFromIDList(pidl)
            pathD = None
            try:
                pathD = path.decode('gbk')
            except Exception as e:
                try:
                    pathD = path.decode('utf-8')
                except Exception as e:
                    raise E().e(e, message="文件夹路径解密错误")
            return pathD
    except Exception as e:
        raise E().e(e, message="打开选择文件夹选择对话框失败")


def select_file():
    """ CreateFileDialog:
            bFileOpen;
            defExt;
            fileName;
            flags;
            filter;
            parent;
    """
    dlg = win32ui.CreateFileDialog(1, None, None, win32con.OFN_HIDEREADONLY | win32con.OFN_OVERWRITEPROMPT, None, None)
    dlg.SetOFNInitialDir('C:')
    dlg.SetOFNTitle("选择文件")
    flag = dlg.DoModal()

    filename = dlg.GetPathName()  # 获取选择的文件名称
    print(filename)


def simple_request_get(url: str, params=None, timeout: int = 60) -> Response:
    """ 简单 get 请求 """
    return requests.get(url, params=params, headers=const.headers,
                        proxies=urllib.request.getproxies(), timeout=(5, timeout))


def open_url(url: str) -> None:
    """ 默认浏览器打开链接 """
    webbrowser.open(url)


def to_json_str(obj: object) -> str:
    """ class对象转json字符串 """
    return json.dumps(obj.__dict__, indent=4, ensure_ascii=False)


def kill_process(pids: List[int], kill_tree: bool = False) -> str:
    """ 杀死进程 """
    joins = ''
    for pid in pids:
        joins += ' -pid {}'.format(pid)
    cmd = 'taskkill -f {} {}'.format('-t' if kill_tree else '', joins)
    result = os.popen(cmd)
    return result.read()


def getpid() -> int:
    """ 获取主进程PID """
    return os.getppid()


def get_request_params(url: str) -> dict:
    """
    从URL中获取请求参数
    :param url:
    :return: 参数元组列表 list of (name, value) tuples
    """
    query = urllib.parse.urlsplit(url).query
    query = dict(urllib.parse.parse_qsl(query))

    # 移除空值
    dict_res = {k: v for k, v in query.items() if v}

    return dict_res


def serialize(tar: typing.Any) -> str:
    """ 对象序列化保存为字节字符串：None -> b'\x80\x04N.' """
    b = pickle.dumps(tar)
    return b.__str__()


def deserialize(tar: str) -> typing.Any:
    """ 字节字符串反序列化为对象：b'\x80\x04N.' -> None """
    b = eval('bytes({})'.format(tar))
    return pickle.loads(b)


def rm_file_dir(path: str) -> bool:
    """ 删除文件夹或文件 """
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        if os.path.isfile(path):
            os.remove(path)
        return True
    except:
        return False


def get_split_value(opt_val: str, delimiter: str, opt_type: type = str) -> list:
    """
    获取多值分割项，通常由分隔符分割每一个值

    :param opt_val: 配置项字符值
    :param delimiter: 分割符
    :param opt_type: 配置的项每个值的数据类型，作为类型转换
    :return list: 配置项的每个值
    """
    if not (opt_val or delimiter):
        return []
    opt_vals = opt_val.split(delimiter)
    # 去除空白字符
    opt_vals = list(map(lambda s: s.strip(), opt_vals))
    # 去除空白项
    opt_vals = list(filter(lambda s: s, opt_vals))
    # 类型转换
    try:
        opt_vals = list(map(lambda s: opt_type(s), opt_vals))
    except:
        return []
    return opt_vals


def get_path_size(path: str) -> int:
    """
    获取文件夹或者文件大小
    :param path: 文件夹 / 文件
    :return: 字节
    """
    size = 0
    if not path or not os.path.exists(path):
        pass
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
    else:
        size = os.path.getsize(path)
    return size


def get_win_valid_filename(filename: str, sub: str = '') -> str:
    """ 获取windows合法文件名 """
    patn = r'[\\/:*?"<>|\r\n]+'
    if sub and re.match(patn, sub): sub = ''
    return re.sub(patn, sub, filename)


def is_network_available() -> bool:
    """ 判断网络是否连通 """
    url = 'baidu.com'
    try:
        popen = os.popen('nslookup {} && exit'.format(url))
        result = popen.read()
        if re.match(r'.*(No response|fec0:0:0:ffff::1|127.0.0.1).*', result, flags=re.I | re.S):
            return False
    except:
        return False
    return True


def set_win_title(title: str, pid: int = None):
    """ 设置窗口标题：不可用 """
    if not pid:
        try:
            win32api.SetConsoleTitle(title)
            return True
        except:
            return False
    hwnd = None
    try:
        hwnd = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False, pid)
        win32gui.SetWindowText(hwnd, title)
        return True
    except Exception as e:
        return False
    finally:
        if hwnd: win32api.CloseHandle(hwnd)
    # hwnd = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False, 5676)
    # print(win32process.GetProcessId(hwnd))
    # win32api.CloseHandle(hwnd)
