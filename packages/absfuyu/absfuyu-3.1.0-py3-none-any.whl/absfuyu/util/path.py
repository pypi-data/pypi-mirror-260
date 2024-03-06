# -*- coding: utf-8 -*-
"""
Absfuyu: Path
-------------
Path related

Version: 1.5.1
Date updated: 24/11/2023 (dd/mm/yyyy)

Feature:
--------
- Directory
- SaveFileAs
"""


# Module level
###########################################################################
__all__ = [
    # "here_location", "location_wrap", "get_all_file_path",
    "Directory",
    "SaveFileAs"
]


# Library
###########################################################################
from datetime import datetime
from functools import partial
import os
from pathlib import Path
import re
import shutil
from typing import Any, List, Literal, Tuple, Union

from absfuyu.logger import logger


# Function
###########################################################################
def here_location(): # Depreciated
    """
    Return current file location
    
    If fail then return current working directory
    """
    try:
        return os.path.abspath(os.path.dirname(__file__))
    except:
        return os.getcwd()
    
    # return os.path.abspath(os.path.dirname(__file__))

def location_wrap(file_location: str): # Depreciated
    """
    This function fix some `current working directory` error and return `abspath`
    """
    assert isinstance(file_location, str), "Must be a string"
    try: 
        here = here_location()
    except:
        here = ""
    return os.path.join(here, file_location)

def get_all_file_path(folder: str, *file_type: str) -> list: # Depreciated
    """
    Return a list of tuple: (path to choosen file type, filename)
    
    - ``folder``: Folder path to search in
    - ``file_type``: File type/extension without the ``"."`` symbol. 
    
    Support multiple file type (separate with ``","`` (coma)) 
    (Example: ``jpg``, ``png``, ``npy``)
    """
    # Check file type
    # If no `file_type` entered then proceed to print available file type
    if len(file_type) < 1:
        available_file_type = []
        for _, _, files in os.walk(folder):
            for file in files:
                temp = re.search(r"\b.*[.](\w+$)\b", file)
                if temp is not None:
                    available_file_type.append(temp[1])
        # print(f"Available file type: {set(available_file_type)}")
        # return list(set(available_file_type))
        # return None
        raise ValueError(f"Available file type: {set(available_file_type)}")

    # Generate regex pattern
    temp_pattern = "|".join(f"[.]{x}" for x in file_type)
    pattern = f"\\b^([\w ]+)({temp_pattern}$)\\b"
    # print("Search pattern: ", pattern)
    
    # Iter through each folder to find file
    file_location = []
    # for root, dirs, files in os.walk(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            result = re.search(pattern, file)
            if result is not None:
                file_location.append((os.path.join(root, file), result[1]))
    return file_location

def here_sniplet():
    """Return current file location code"""
    snip = """\
import os
here = os.path.abspath(os.path.dirname(__file__))

from pathlib import Path
here = Path(__file__)
"""
    return snip


# Class
###########################################################################
class Directory:
    """
    Some shortcuts for directory
    
    - list_structure
    - delete, rename, copy, move
    - zip
    """
    def __init__(
            self,
            source_path: Union[str, Path],
            create_if_not_exist: bool = False,
        ) -> None:
        """
        source_path: Source folder
        create_if_not_exist: Create directory when not exist
        """
        self.source_path = Path(source_path).absolute()
        if create_if_not_exist:
            self.source_path.mkdir(exist_ok=True)
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.source_path})"
    def __repr__(self) -> str:
        return self.__str__()
    
    # Rename
    def rename(self, new_name: str) -> None:
        """
        Rename directory
        
        Parameters
        ----------
        new_name : str
            Name only (not the entire path)
        """
        try:
            logger.debug(f"Renaming to {new_name}...")
            self.source_path.rename(
                self.source_path.parent.joinpath(new_name)
            )
            logger.debug(f"Renaming to {new_name}...DONE")
        except Exception as e:
            logger.error(e)
    
    # Copy
    def copy(self, dst: Path) -> None:
        """
        Copy entire directory

        Parameters
        ----------
        dst : Path
            Destination
        """
        logger.debug(f"Copying to {dst}...")
        try:
            try:
                shutil.copytree(self.source_path, Path(dst), dirs_exist_ok=True)
            except:
                shutil.copytree(self.source_path, Path(dst))
            logger.debug(f"Copying to {dst}...DONE")
        except Exception as e:
            logger.error(e)
    
    # Move
    def move(self, dst: Path) -> None:
        """
        Move entire directory

        Parameters
        ----------
        dst : Path
            Destination
        """
        try:
            logger.debug(f"Moving to {dst}...")
            shutil.move(self.source_path, Path(dst))
            logger.debug(f"Moving to {dst}...DONE")
        except Exception as e:
            logger.error(e)

    # Directory structure
    def _list_dir(self, *ignore: str) -> List[Path]:
        """List all directories and files"""
        logger.debug(f"Base folder: {self.source_path.name}")

        temp = self.source_path.glob("**/*")
        # No ignore rules
        if len(ignore) == 0:
            return [x.relative_to(self.source_path) for x in temp]

        # With ignore rules
        ignore_pattern = "|".join(ignore)
        logger.debug(f"Ignore pattern: {ignore_pattern}")
        return [x.relative_to(self.source_path) for x in temp if re.search(ignore_pattern, x.name) is None]

    def _separate_dir_and_files(
            self,
            list_of_paths: List[Path],
            *,
            tab_symbol: str = None,
            sub_dir_symbol: str = None
        ) -> List[str]:
        """
        Separate dir and file and transform into folder structure
        
        list_of_paths: List of paths
        tab_symbol: Tab symbol
        sub_dir_symbol: Sub-directory symbol
        """
        if not tab_symbol:
            tab_symbol = "\t"
        if not sub_dir_symbol:
            sub_dir_symbol = "|-- "

        temp = sorted([str(x).split("/") for x in list_of_paths]) # Linux
        if max(map(len, temp)) == 1:
            temp = sorted([str(x).split("\\") for x in list_of_paths]) # Windows

        return [f"{tab_symbol*(len(x)-1)}{sub_dir_symbol}{x[-1]}" for x in temp]

    def list_structure(self, *ignore: str) -> str:
        """
        List folder structure

        Parameters
        ----------
        ignore : str
            Tuple contains patterns to ignore
        
        Returns
        -------
        str
            Directory structure


        Example (For typical python library):
        -------------------------------------
        >>> test = Directory(<source path>)
        >>> test.list_structure(
                "__pycache__",
                ".pyc",
                "__init__", 
                "__main__",
            )
        ...
        """
        temp = self._list_dir(*ignore)
        out = self._separate_dir_and_files(temp)
        return "\n".join(out)
    
    def list_structure_pkg(self) -> str:
        """
        List folder structure of a typical python package
        
        Returns
        -------
        str
            Directory structure
        """
        return self.list_structure("__pycache__", ".pyc")

    # Delete folder
    def _mtime_folder(self) -> List[Tuple[Path, datetime]]:
        """Get modification time of file/folder"""
        return [(x, datetime.fromtimestamp(x.stat().st_mtime)) for x in self.source_path.glob("*")]

    @staticmethod
    def _delete_files(list_of_files: List[Path]) -> None:
        """
        Delete files/folders
        """
        for x in list_of_files:
            x = Path(x).absolute()
            logger.debug(f"Removing {x}...")
            try:
                if x.is_dir():
                    shutil.rmtree(x)
                else:
                    x.unlink()
                logger.debug(f"Removing {x}...REMOVED")
            except:
                logger.error(f"Removing {x}...FAILED")

    @staticmethod
    def _date_filter(
            value: Tuple[Path, datetime], 
            period: Literal["Y", "M", "D"] = "Y"
        ) -> bool:
        """
        Filter out file with current Year|Month|Day
        """
        period = period.upper().strip()
        data = {
            "Y": value[1].year, 
            "M": value[1].month, 
            "D": value[1].day
        }
        now = datetime.now()
        ntime = {
            "Y": now.year, 
            "M": now.month, 
            "D": now.day
        }
        return data[period] != ntime[period]

    def delete(
            self, 
            entire: bool = False,
            *,
            based_on_time: bool = False,
            keep: Literal["Y", "M", "D"] = "Y"
        ) -> None:
        """
        Deletes everything

        Parameters
        ----------
        entire : bool
            | ``True``: Deletes the folder itself
            | ``False``: Deletes content inside only
            | (Default: ``False``)
        
        based_on_time : bool
            | ``True``: Deletes everything except ``keep`` period
            | ``False``: Works normal
            | (Default: ``False``)
        
        keep : Literal["Y", "M", "D"]
            Delete all file except current ``Year`` | ``Month`` | ``Day``
        """
        try:
            logger.info(f"Removing {self.source_path}...")
            
            if entire:
                shutil.rmtree(self.source_path)
            else:
                if based_on_time:
                    filter_func = partial(self._date_filter, period=keep)
                    self._delete_files([x[0] for x in filter(filter_func, self._mtime_folder())])
                else:
                    self._delete_files(map(lambda x: x[0], self._mtime_folder()))
            
            logger.info(f"Removing {self.source_path}...COMPLETED")
        except:
            logger.error(f"Removing {self.source_path}...FAILED")

    # Zip
    def compress(self, *, format: str = "zip") -> None:
        """
        Compress the directory (Default: Create ``.zip`` file)
        
        Parameters
        ----------
        format : Literal["zip", "tar", "gztar", "bztar", "xztar"]
            - ``zip``: ZIP file (if the ``zlib`` module is available).
            - ``tar``: Uncompressed tar file. Uses POSIX.1-2001 pax format for new archives.
            - ``gztar``: gzip'ed tar-file (if the ``zlib`` module is available).
            - ``bztar``: bzip2'ed tar-file (if the ``bz2`` module is available).
            - ``xztar``: xz'ed tar-file (if the ``lzma`` module is available).
        """
        logger.debug(f"Zipping {self.source_path}...")
        try:
            zip_name = self.source_path.parent.joinpath(self.source_path.name)
            shutil.make_archive(zip_name, format=format, root_dir=self.source_path)
            logger.debug(f"Zipping {self.source_path}...DONE")
        except:
            logger.error(f"Zipping {self.source_path}...FAILED")


class SaveFileAs:
    """File as multiple file type"""
    def __init__(
            self,
            data: Any,
            *,
            encoding: Union[str, None] = "utf-8"
        ) -> None:
        """
        :param encoding: Default: utf-8
        """
        self.data = data
        self.encoding = encoding
    def __str__(self) -> str:
        return f"{self.__class__.__name__}()"
    def __repr__(self) -> str:
        return self.__str__()

    def to_txt(self, path: Union[str, Path]) -> None:
        """
        Save as ``.txt`` file
        
        Parameters
        ----------
        path : Path
            Save location
        """
        with open(path, "w", encoding=self.encoding) as file:
            file.writelines(self.data)
    
    # def to_pickle(self, path: Union[str, Path]) -> None:
    #     """
    #     Save as .pickle file
        
    #     :param path: Save location
    #     """
    #     from absfuyu.util.pkl import Pickler
    #     Pickler.save(path, self.data)

    # def to_json(self, path: Union[str, Path]) -> None:
    #     """
    #     Save as .json file
        
    #     :param path: Save location
    #     """
    #     from absfuyu.util.json_method import JsonFile
    #     temp = JsonFile(path, sort_keys=False)
    #     temp.save_json()


# Run
###########################################################################
if __name__ == "__main__":
    logger.setLevel(10)
    