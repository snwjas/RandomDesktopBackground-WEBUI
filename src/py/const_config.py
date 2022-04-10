# -*-coding:utf-8-*-

"""
常量定义

@author Myles Yang
"""
import os
import sys
from enum import Enum

# 程序名称
app_name = '随机桌面壁纸'
app_name_en = "RandomDesktopBackground"

# webui 地址
host = '127.6.6.6'

# webui 端口
port = 23333

# webui服务路径
server = 'http://{}:{}'.format(host, port)

# 对话框标题
dialog_title = '来自"{}"的提示'.format(app_name)

app_fullpath = os.path.abspath(sys.argv[0])
app_dirname = os.path.dirname(app_fullpath)

# 壁纸保存目录
bg_srcpath = 'wallpapers'

# 运行日志保存目录
log_srcpath = 'log'

# 收藏文件夹
favorite_srcpath = 'favorite'

# 数据库名称
db_name = 'rdbdb.db'


class Key:
    """ 配置key定义 """

    class Run(Enum):
        BPID = 'run.bpid'
        FPID = 'run.fpid'
        WORKDIR = 'run.workdir'
        STARTUP = 'run.startup'

        PROXY = 'run.proxy'
        _PROXY_NONE = 'none'
        _PROXY_SYSTEM = 'system'

        ROTATION = 'run.rotation'
        _ROTATION_LOCAL = 'local'
        _ROTATION_NETWORK = 'network'
        LOCAL__DISORDER = 'run.local.disorder'

    class Api(Enum):
        NAME = 'api.name'

        WALLHAVEN__URL = 'api.wallhaven.url'
        WALLHAVEN__APIKEY = 'api.wallhaven.apikey'

        CUSTOM = 'api.custom.url'
        _NAME_WALLHAVEN = 'wallhaven'
        _NAME_CUSTOM = 'custom'

    class Task(Enum):
        SECONDS = 'task.seconds'
        CURRENT = 'task.current'
        MODE = 'task.mode'
        THREADS = 'task.threads'
        RND_SLEEP_L = 'task.rnd_sleep_l'
        RND_SLEEP_R = 'task.rnd_sleep_r'
        RETAIN_BGS = 'task.retain_bgs'

        MAX_RETAIN_MB = 'task.max_retain_mb'
        _MODE_MULTIPLE = 'multiple'
        _MODE_SINGLE = 'single'

    class Hotkey(Enum):
        ENABLE = 'hotkey.enable'
        PREV_BG = 'hotkey.prev_bg'
        NEXT_BG = 'hotkey.next_bg'
        FAV_BG = 'hotkey.fav_bg'
        LOC_BG = 'hotkey.loc_bg'

    class CtxMenu(Enum):
        ENABLE = 'ctxmenu.enable'
        PREV_BG = 'ctxmenu.prev_bg'
        NEXT_BG = 'ctxmenu.next_bg'
        FAV_BG = 'ctxmenu.fav_bg'
        LOC_BG = 'ctxmenu.loc_bg'


# wallhaven请求api
wallhaven_api = 'https://wallhaven.cc/api/v1/search'
# wallhaven网站
wallhaven_website = 'https://wallhaven.cc/search'

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6776.400 QQBrowser/10.3.2577.400'
}

# favicon
favicon = 'AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAgBAAABMLAAATCwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP+fQir/nT+d/55Apv+eQJ7/nkCe/55Anv+eQJ7/nkCe/55Anv+eQJ7/nkCe/59Anf+fQJ3/n0Cd/59Anf+fQJ3/n0Cd/59Anf+fQJ3/n0Cl/55Anf+fQCwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/oEJZ/59B5/+eQP//nkD//55A//+eQP//nkD//55A//+eQP//nkD//55A//+eQP//nkD//55A//+eQP//nkD//55A//+eQP//nkD//55A//+eQP//nkD//55A4f+fQFIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP+dP5H/nkD//55A//+eQP//nkD//55A//+eQP//nkD//55A//+eQP//nkD//55A//+eQP//nkD//55A//+eQP//nkD//55A//+eQP//nkD//55A//+eQP//nkD//55AjwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/55AkP+eQP//n0D//55A//+eQP//nkD//55A//+eQP//nkD//55A//+eQP//nkD//55A//+eQP//nkD//55A//+eQP//nkD//55A//+eQP//nkD//55A//+eQP//nkCRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/nkCZ/55A//+dQeL/nkD//55A//+eQP//nkD//55A//+eQP//nkD//55A//+eQP//nkD//55A//+eQP//nkD//55A//+eQP//nkD//55A//+eQP//nUDi/55A//+eQJkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP+fP6r/oDz//5dNVP+aSK7/nz3//55A//+eQP//nkD//55A//+eQP//nkD//55A//+eQP//nkD//55A//+eQP//nkD//55A//+eQP//mkP//6k5r/+rN1X/mUP//55AqgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/55Ap/+eP///m0M7/59BDv+gPf//nkD//55A//+eQP//nj///58+7/+eQPf/nkD//55A//+eQP//nkD//55A//+eQP//nkD//55A//+eQ///oT8R/589Ov+dQf//nkCnAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/nkCn/55A//+cPlkAAAAA/51Ge/+eP///nkD//55A//+eQej/nUMJ/54/mf+eQP//nkD//55A//+e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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/////////////////////////////////AAAP/gAAB/4AAAf+AAAH/gAAB/4AAAf+wAA3/sEAN/5jgGf+d8Dn/n/A5/5/4ef+f/Pn/mf/t/7D/jf+w/43/uf/9/5//+f+AAAH/wAAD////////////////////////////////8='

# 数据库创建SQL
db_init_sql = R"""
PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for config
-- ----------------------------
DROP TABLE IF EXISTS "config";
CREATE TABLE "config" (
  "key" text(127) NOT NULL,
  "value" text DEFAULT '',
  "pytype" text(15) DEFAULT 'str',
  "defaults" text DEFAULT NULL,
  "comment" text DEFAULT '',
  "enable" integer(1) DEFAULT 1,
  "utime" char(19) DEFAULT (datetime('now','localtime')),
  "ctime" char(19) DEFAULT (datetime('now','localtime')),
  PRIMARY KEY ("key")
);

-- ----------------------------
-- Records of config
-- ----------------------------
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('run.bpid', '-1', 'int', 'b''\x80\x04\x95\x06\x00\x00\x00\x00\x00\x00\x00J\xff\xff\xff\xff.''', '运行：后台运行程序的PID');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('run.fpid', '-1', 'int', 'b''\x80\x04\x95\x06\x00\x00\x00\x00\x00\x00\x00J\xff\xff\xff\xff.''', '运行：前台运行程序的PID');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('run.startup', 'False', 'bool', 'b''\x80\x04\x89.''', '运行：是否开机启动');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('run.workdir', '', 'str', 'b''\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00\x8c\x00\x94.''', '运行：程序工作目录');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('run.proxy', 'none', 'str', 'b''\x80\x04\x95\n\x00\x00\x00\x00\x00\x00\x00\x8c\x06system\x94.''', '运行：用户代理[none|system]');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('run.rotation', 'network', 'str', 'b''\x80\x04\x95\x0b\x00\x00\x00\x00\x00\x00\x00\x8c\x07network\x94.''', '运行：轮播方式[network|local]');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('run.local.disorder', 'True', 'bool', 'b''\x80\x04\x88.''', '运行：本地轮播是否为无序');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('api.name', 'wallhaven', 'str', 'b''\x80\x04\x95\r\x00\x00\x00\x00\x00\x00\x00\x8c\twallhaven\x94.''', 'API：图源名[wallhaven|custom]');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('api.wallhaven.url', 'https://wallhaven.cc/search?categories=111&purity=110&sorting=random&order=desc&resolutions=1920x1080', 'str', 'b''\x80\x04\x95S\x00\x00\x00\x00\x00\x00\x00\x8cOhttps://wallhaven.cc/search?categories=111&purity=110&sorting=random&order=desc&resolutions=1920x1080\x94.''', 'API：wallhaven图源地址');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('api.wallhaven.apikey', '', 'str', 'b''\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00\x8c\x00\x94.''', 'API：wallhaven API Key');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('api.custom.url--536007639', 'https://api.btstu.cn/sjbz/?lx=suiji', 'str', NULL, '');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('api.custom.url--542024925', 'https://api.btstu.cn/sjbz/?lx=meizi', 'str', NULL, '');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('api.custom.url--302158599', 'https://api.btstu.cn/sjbz/?lx=dongman', 'str', NULL, '');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('task.seconds', '1440', 'int', 'b''\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00M\xa0\x05.''', '任务：切换频率');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('task.current', '0', 'int', 'b''\x80\x04K\x00.''', '任务：当前壁纸下标');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('task.mode', 'multiple', 'str', 'b''\x80\x04\x95\x0c\x00\x00\x00\x00\x00\x00\x00\x8c\x08multiple\x94.''', '任务：壁纸拉取模式[multiple|single]');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('task.threads', '2', 'int', 'b''\x80\x04K\x02.''', '任务：壁纸拉取时使用线程数量');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('task.rnd_sleep_l', '0.5', 'float', 'b''\x80\x04\x95\n\x00\x00\x00\x00\x00\x00\x00G?\xe0\x00\x00\x00\x00\x00\x00.''', '任务：壁纸拉取时随机停顿间隔时间左');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('task.rnd_sleep_r', '5', 'int', 'b''\x80\x04K\x05.''', '任务：壁纸拉取时随机停顿间隔时间右');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('task.retain_bgs', 'False', 'bool', 'b''\x80\x04\x89.''', '任务：是否保留已经拉取下来的壁纸');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('task.max_retain_mb', '-1', 'int', 'b''\x80\x04\x95\x06\x00\x00\x00\x00\x00\x00\x00J\xff\xff\xff\xff.''', '任务：壁纸保留最大占用内存');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('hotkey.enable', 'False', 'bool', 'b''\x80\x04\x89.''', '热键：是否启用全局热键');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('hotkey.prev_bg', '', 'str', 'b''\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00\x8c\x00\x94.''', '热键：切换到上一张壁纸');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('hotkey.next_bg', '', 'str', 'b''\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00\x8c\x00\x94.''', '热键：切换到下一张壁纸');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('hotkey.fav_bg', '', 'str', 'b''\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00\x8c\x00\x94.''', '热键：收藏当前壁纸');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('hotkey.loc_bg', '', 'str', 'b''\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00\x8c\x00\x94.''', '热键：定位到当前壁纸文件');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('ctxmenu.enable', 'False', 'bool', 'b''\x80\x04\x89.''', '桌面右键菜单：是否启用桌面右键菜单');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('ctxmenu.prev_bg', 'False', 'bool', 'b''\x80\x04\x89.''', '桌面右键菜单：是否启用切换上一张壁纸');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('ctxmenu.next_bg', 'False', 'bool', 'b''\x80\x04\x89.''', '桌面右键菜单：是否启用切换下一张壁纸');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('ctxmenu.fav_bg', 'False', 'bool', 'b''\x80\x04\x89.''', '桌面右键菜单：是否启用收藏当前壁纸');
INSERT INTO config ("key", value, pytype, "defaults", comment) VALUES('ctxmenu.loc_bg', 'False', 'bool', 'b''\x80\x04\x89.''', '桌面右键菜单：是否启用定位到当前壁纸文件');

-- ----------------------------
-- Indexes structure for table config
-- ----------------------------
CREATE UNIQUE INDEX "idx_key"
ON "config" (
  "KEY" ASC
);

-- ----------------------------
-- Triggers structure for table config
-- ----------------------------
CREATE TRIGGER "config.onupdate"
AFTER UPDATE
ON "config"
BEGIN
  update config
	set UTIME = datetime('now','localtime')
	where key = (case when old.key = new.key then old.key else new.key end);
END;

PRAGMA foreign_keys = true;
"""
