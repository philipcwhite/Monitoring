import sys 
from cx_Freeze import setup, Executable

#python setup.py build

build_exe_options = {"packages": ['asyncio','win32timezone'], "excludes": ["tkinter"]}

setup(
    name = "Agent Service",
    version = "0.1",
    description = "A Windows service for Monitoring",
    options = {"build_exe": build_exe_options},
    executables = [Executable("agent_service.py", base = "Win32GUI")])