import sys 
from cx_Freeze import setup, Executable

#python setup.py build

build_exe_options = {"packages": ['asyncio','win32timezone','pymysql'], "excludes": ["tkinter"]}

setup(
    name = "Agent Collector",
    version = "0.1",
    description = "A Windows service for Monitoring",
    options = {"build_exe": build_exe_options},
    executables = [Executable("collect_service.py", base = "Win32GUI")])