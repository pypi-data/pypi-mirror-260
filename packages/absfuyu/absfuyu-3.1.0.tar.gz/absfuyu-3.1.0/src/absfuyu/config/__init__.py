"""
Absfuyu: Configuration
----------------------
Package configuration module

Version: 2.0.1
Date updated: 24/11/2023 (dd/mm/yyyy)
"""


# Module level
###########################################################################
__all__ = [
    "ABSFUYU_CONFIG",
    "Config",
    # "Setting"
]


# Library
###########################################################################
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from absfuyu.core import CONFIG_PATH
from absfuyu.util.json_method import JsonFile


# Setting
###########################################################################
_SPACE_REPLACE = "-" # Replace " " character in setting name


# Class
###########################################################################
class Setting:
    """Setting"""
    def __init__(
            self,
            name: str,
            value: Any,
            default: Any,
            help_: str = ""
        ) -> None:
        """
        :param name: Name of the setting
        :param value: Value of the setting
        :param default: Default value of the setting
        :param help: Description of the setting
        """
        self.name = name
        self.value = value
        self.default = default
        self.help = help_
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name}: {self.value})"
    def __repr__(self) -> str:
        return self.__str__()
    
    @classmethod
    def from_dict(cls, dict_data: Dict[str, Dict[str, Any]]):
        """Convert ``dict`` into ``Setting`` (``len==1`` only)"""
        name = list(dict_data.keys())[0]
        _val = list(dict_data.values())[0]
        value: Any = _val.get("value")
        default: Any = _val.get("default")
        help_: str = _val.get("help")
        return cls(name, value, default, help_)
    
    def reset(self) -> None:
        """
        Reset setting to default value 
        (``Setting.value = Setting.default``)
        """
        self.value = self.default
    
    def update_value(self, value: Any) -> None:
        """Update current value"""
        self.value = value

    def to_dict(self) -> Dict[str, Dict[str, Any]]:
        """Convert ``Setting`` into ``dict``"""
        output = {
            self.name: {
                "default": self.default,
                "help": self.help,
                "value": self.value
            }
        }
        return output


class Config:
    """
    Config handling
    """
    def __init__(self, config_file: Path, name: Optional[str] = None) -> None:
        """
        config_file: Path to `.json` config file
        """
        self.config_path = config_file
        self.json_engine = JsonFile(self.config_path)

        if name:
            self.name = name
        else:
            self.name = self.config_path.name

        # Data
        self.settings: List[Setting] = None
        self.version: dict = None
        self._fetch_data() # Load data

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.config_path.name})"
    def __repr__(self) -> str:
        return self.__str__()
    
    # Data prepare and export
    def _fetch_data(self) -> None:
        """Load data from ``self.config_file`` file"""
        data = self.json_engine.load_json()
        settings: dict = data.get("setting")
        self.settings = [Setting.from_dict({k: v}) for k, v in settings.items()]
        self.version = data.get("version")
    
    def _prepare_data(self) -> Dict[str, dict]:
        """Prepare data to save config"""
        settings = dict()
        for x in self.settings:
            settings.update(x.to_dict())

        out = {
            "setting": settings,
            "version": self.version
        }
        return out
    
    def save(self) -> None:
        """Save config to ``.json`` file"""
        self.json_engine.update_data(
            self._prepare_data()
        )
        self.json_engine.save_json()

    # Setting method
    def _get_setting(self, name: str):
        """Get setting"""
        name = name.strip().lower().replace(" ", _SPACE_REPLACE)
        setting_list = [x.name for x in self.settings]
        if name in setting_list:
            for x in self.settings:
                if x.name.startswith(name):
                    return x
        else:
            raise ValueError(f"Setting list: {setting_list}")
    
    def reset_config(self) -> None:
        """Reset all settings to default value"""
        [x.reset() for x in self.settings]
        self.save()
    
    def show_settings(self) -> None:
        """
        Print a list of available settings 
        (wrapper for ``Config.settings``)
        """
        return self.settings

    def change_setting(self, name: str, value: Any) -> None:
        """
        Change ``Setting`` (if available)
        
        Parameters
        ----------
        name : str
            Name of the setting
        
        value : Any
            Value of the setting
        """
        name = name.strip().lower().replace(" ", _SPACE_REPLACE)
        setting_list = [x.name for x in self.settings]
        if name in setting_list:
            for x in self.settings:
                if x.name.startswith(name):
                    x.update_value(value)
                    break
        else:
            raise ValueError(f"Setting list: {setting_list}")
        self.save()
    
    def toggle_setting(self, name: str) -> None:
        """
        Special ``change_setting()`` method. 
        Turn on/off if ``type(<setting>) is bool``

        Parameters
        ----------
        name : str
            Name of the setting
        """
        # Get setting
        setting = self._get_setting(name)
        setting_value: bool = setting.value

        # Change value
        try:
            self.change_setting(name, not setting_value)
        except:
            raise SystemExit("This setting is not type: bool")
    
    def add_setting(self, name: str, value: Any, default: Any, help_: str = "") -> None:
        """
        Add ``Setting`` if not exist
        
        Parameters
        ----------
        name : str
            Name of the setting

        value : Any
            Value of the setting

        default : Any
            Default value of the setting

        help_ : str
            Description of the setting (Default: None)
        """
        name = name.strip().lower().replace(" ", _SPACE_REPLACE)
        new_setting = Setting(name, value, default, help_)
        if new_setting not in self.settings:
            self.settings.append(new_setting)
        self.save()
    
    def del_setting(self, name: str) -> None:
        """
        Delete ``Setting``
        
        Parameters
        ----------
        name : str
            Name of the setting
        """
        name = name.strip().lower().replace(" ", _SPACE_REPLACE)
        self.settings = [x for x in self.settings if not x.name == name]
        self.save()

    def welcome(self) -> None:
        """Run first-run script (if any)"""
        self.change_setting("first-run", False)

    # Version
    def update_version(self, version_data: Dict[str, Union[str, int]]):
        """
        Update version

        Parameters
        ----------
        version_data : dict[str, str | int]
            Version data
        """
        self.version = version_data
        self.save()


# Init
###########################################################################
ABSFUYU_CONFIG = Config(CONFIG_PATH)


# Run
###########################################################################
if __name__ == "__main__":
    pass