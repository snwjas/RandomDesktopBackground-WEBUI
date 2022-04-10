chcp 65001
@echo off

title Python项目打包.exe

cls

@REM 打包依赖 pyinstaller
@REM pip install pyinstaller

::gcc -mwindows cmdtransmitter.c -o cmdtransmitter.exe

if exist build rd /S /Q build

if exist dist rd /S /Q dist

..\venv\Scripts\pyinstaller application.spec --clean -y

echo.&&echo 打包完成！程序位于当前目录的dist文件夹下。

echo.&&set /p tips=按0键回车打开该目录...

if %tips% equ 0 explorer /e, dist
