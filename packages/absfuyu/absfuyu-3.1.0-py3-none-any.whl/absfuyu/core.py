"""
Absfuyu: Core
-------------
Contain type hints and other stuffs

Version: 2.1.9
Date updated: 27/11/2023 (dd/mm/yyyy)
"""


# Module Package
###########################################################################
__all__ = [
    # module
    "ModulePackage",
    "ModuleList",
    # color
    "Color",
    "CLITextColor",
    # path
    "CORE_PATH",
    "CONFIG_PATH",
    "DATA_PATH",
]

ModulePackage = ["all", "cli", "beautiful", "extra", "res", "full", "dev"]
ModuleList = [
    "config",
    "extensions",
    "fun",
    "game",
    "general",
    "pkg_data",
    "sort",
    "tools",
    "util",
    "version",
]


# Library
###########################################################################
from pathlib import Path
# import sys

# if sys.version_info.minor >= 10:
#     from importlib.resources import files
# else:
#     try:
#         from importlib_resources import files
#     except:
#         raise ImportError("Please install importlib-resources")


try:
    import colorama as __colorama
except ImportError:
    __colorama = None


# Color - colorama
###########################################################################
if __colorama is not None:
    # __colorama.init(autoreset=True)
    Color = {
        "green": __colorama.Fore.LIGHTGREEN_EX,
        "GREEN": __colorama.Fore.GREEN,
        "blue": __colorama.Fore.LIGHTCYAN_EX,
        "BLUE": __colorama.Fore.CYAN,
        "red": __colorama.Fore.LIGHTRED_EX,
        "RED": __colorama.Fore.RED,
        "yellow": __colorama.Fore.LIGHTYELLOW_EX,
        "YELLOW": __colorama.Fore.YELLOW,
        "reset": __colorama.Fore.RESET,
    }
else:
    Color = {
        "green": "",
        "GREEN": "",
        "blue": "",
        "BLUE": "",
        "red": "",
        "RED": "",
        "yellow": "",
        "YELLOW": "",
        "reset": "",
    }


class CLITextColor:
    """Color code for text in terminal"""

    WHITE = "\x1b[37m"
    BLACK = "\x1b[30m"
    BLUE = "\x1b[34m"
    GRAY = "\x1b[90m"
    GREEN = "\x1b[32m"
    RED = "\x1b[91m"
    DARK_RED = "\x1b[31m"
    MAGENTA = "\x1b[35m"
    YELLOW = "\x1b[33m"
    RESET = "\x1b[39m"


# Path
###########################################################################
# CORE_PATH = Path(os.path.abspath(os.path.dirname(__file__)))
CORE_PATH = Path(__file__).parent.absolute()
# CORE_PATH = files("absfuyu")
CONFIG_PATH = CORE_PATH.joinpath("config", "config.json")
DATA_PATH = CORE_PATH.joinpath("pkg_data")


# Run
###########################################################################
if __name__ == "__main__":
    print(CORE_PATH)