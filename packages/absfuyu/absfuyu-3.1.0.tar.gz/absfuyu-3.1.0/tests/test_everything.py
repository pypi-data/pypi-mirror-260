"""
Test: Everything

Version: 1.1.18
Date updated: 06/03/2024 (dd/mm/yyyy)
"""


# Library
###########################################################################
import pytest

from absfuyu import everything as ab

# --- Loading test --------------------------------------------------------
# from absfuyu.core import *
from absfuyu.core import (
    ModulePackage, ModuleList,
    Color, CLITextColor,
    CORE_PATH, CONFIG_PATH, DATA_PATH
)
# from absfuyu.logger import *
from absfuyu.logger import logger, LogLevel, compress_for_log
from absfuyu.sort import (
    selection_sort, insertion_sort,
    alphabetAppear,
    linear_search, binary_search
)
from absfuyu.version import (
    __version__,
    Version, PkgVersion, Bumper,
    ReleaseLevel, ReleaseOption,
    _AbsfuyuPackage
)

# --- Sub-package ---
from absfuyu.general import Dummy, ClassBase
from absfuyu.general.content import ContentLoader, Content, LoadedContent # Has unidecode
from absfuyu.general.data_extension import Text, IntNumber, ListExt, DictExt
from absfuyu.general.generator import Charset, Generator
from absfuyu.general.human import BloodType, Human, Person # Has python-dateutil

from absfuyu.config import ABSFUYU_CONFIG, Config, Setting, _SPACE_REPLACE

from absfuyu.extensions import *
from absfuyu.extensions.beautiful import beautiful_output, demo # Has rich
from absfuyu.extensions.extra import *
from absfuyu.extensions.extra.data_analysis import ( # Has pandas, numpy
    summary, equalize_df, compare_2_list, rename_with_dict,
    PLTFormatString,
    _DictToAtrr,
    MatplotlibFormatString,
    DataAnalystDataFrame, CityData, SplittedDF
)

from absfuyu.fun import zodiac_sign, im_bored, force_shutdown, happy_new_year
from absfuyu.fun.tarot import Tarot, TarotCard
from absfuyu.fun.WGS import WGS

from absfuyu.game import game_escapeLoop, game_RockPaperScissors
from absfuyu.game.sudoku import Sudoku
from absfuyu.game.tictactoe import *
from absfuyu.game.wordle import Wordle # Has requests

from absfuyu.pkg_data import PkgData, PACKAGE_DATA, DataList

from absfuyu.tools import *
from absfuyu.tools.converter import ChemistryElement, Text2Chemistry, Str2Pixel, Base64EncodeDecode
from absfuyu.tools.keygen import Keygen
from absfuyu.tools.obfuscator import Obfuscator, ObfuscatorLibraryList
from absfuyu.tools.stats import ListStats
from absfuyu.tools.web import soup_link, gen_random_commit_msg # Has bs4, requests

from absfuyu.util import get_installed_package, set_max, set_min, set_min_max
from absfuyu.util.api import APIRequest, ping_windows # Has requests
from absfuyu.util.json_method import JsonFile
from absfuyu.util.lunar import LunarCalendar
from absfuyu.util.path import Directory, SaveFileAs
from absfuyu.util.performance import measure_performance, source_this, var_check
from absfuyu.util.pkl import Pickler
from absfuyu.util.zipped import Zipper


# Test
###########################################################################
# def test_ev():
#     assert ab.__IS_EVERYTHING is True

def test_everything():
    assert True