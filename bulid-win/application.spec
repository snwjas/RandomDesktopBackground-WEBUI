# -*- mode: python ; coding: utf-8 -*-

import os

block_cipher = None

root_path = os.path.abspath(os.path.dirname(os.getcwd()))
src_path = os.path.join(root_path, 'src', 'py')


def get_module_path(*filename):
    return os.path.join(src_path, *filename)


a = Analysis([get_module_path('application.py'),
              get_module_path('args_definition.py'),
              get_module_path('component.py'),
              get_module_path('configurator.py'),
              get_module_path('const_config.py'),
              get_module_path('controller.py'),
              get_module_path('dao.py'),
              get_module_path('get_background.py'),
              get_module_path('service.py'),
              get_module_path('set_background.py'),
              get_module_path('utils.py'),
              get_module_path('vo.py'),
              get_module_path('webapp.py'),
              ],
             pathex=[],
             binaries=[],
             datas=[
                 ('cmdtransmitter.exe', '.'),
                 (os.path.join(root_path, 'rdbdb.db'), '.'),
                 (os.path.join(src_path, 'webui'), 'webui'),
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='随机桌面壁纸',
          version='version.rc',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          resources=[],
          upx=True,
          console=False,
          icon=['favicon.ico','pre.ico','nxt.ico','fav.ico','loc.ico'])

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='随机桌面壁纸')
