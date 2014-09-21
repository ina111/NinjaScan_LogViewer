import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "sys", "numpy",
					 "PySide.QtCore", "PySide.QtGui", "matplotlib.pyplot",
                     "matplotlib.backends"],
					 "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "NinjScanLogViewer",
        version = "1.0",
        description = "NinjaScan Log file rapid viewer",
        author = "Takahiro Inagawa",
        options = {"build_exe": build_exe_options},
        executables = [Executable("NinjaScanViewer.py",
        	icon = 'NinjaScanLogo.ico',
        	base=base)])