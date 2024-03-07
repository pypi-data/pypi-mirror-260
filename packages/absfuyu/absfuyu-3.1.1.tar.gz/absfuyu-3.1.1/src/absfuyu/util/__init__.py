"""
Absufyu: Utilities
------------------
Some random utilities

Version: 1.4.4
Date updated: 24/11/2023 (dd/mm/yyyy)
"""


# Library
###########################################################################
import pkgutil
# import sys
from typing import Union

from absfuyu.logger import logger


# Function
###########################################################################
def get_installed_package():
    """
    Return a list of installed packages

    Returns
    -------
    list[str]
        List of installed packages
    """
    iter_modules = list({module.name for module in pkgutil.iter_modules() if module.ispkg})
    # builtin = sys.builtin_module_names
    # return set.union(iter_modules, builtin)
    return sorted(iter_modules)


def set_min(
        current_value: Union[int, float],
        *,
        min_value: Union[int, float] = 0,
    ) -> Union[int, float]:
    """
    Return ``min_value`` when ``current_value`` < ``min_value``

    Parameters
    ----------
    current_value : int | float
        Current value
    
    min_value : int | float
        Minimum value 
        (Default: ``0``)
    
    Returns
    -------
    int | float
        Analyzed value


    Example:
    --------
    >>> set_min(-1)
    0
    """
    if current_value < min_value:
        current_value = min_value
    return current_value

def set_max(
        current_value: Union[int, float],
        *,
        max_value: Union[int, float] = 100,
    ) -> Union[int, float]:
    """
    Return ``max_value`` when ``current_value`` > ``max_value``

    Parameters
    ----------
    current_value : int | float
        Current value
    
    max_value : int | float
        Maximum value 
        (Default: ``100``)
    
    Returns
    -------
    int | float
        Analyzed value


    Example:
    --------
    >>> set_max(101)
    100
    """
    if current_value > max_value:
        current_value = max_value
    return current_value

def set_min_max(
        current_value: Union[int, float],
        *,
        min_value: Union[int, float] = 0,
        max_value: Union[int, float] = 100
    ) -> Union[int, float]:
    """
    Return ``min_value`` | ``max_value`` when ``current_value``
    is outside ``[min_value, max_value]``

    Parameters
    ----------
    current_value : int | float
        Current value
    
    min_value : int | float
        Minimum value 
        (Default: ``0``)
    
    max_value : int | float
        Maximum value 
        (Default: ``100``)
    
    Returns
    -------
    int | float
        Analyzed value


    Example:
    --------
    >>> set_min_max(808)
    100
    """
    current_value = set_min(current_value, min_value=min_value)
    current_value = set_max(current_value, max_value=max_value)
    return current_value


# Run
###########################################################################
if __name__ == "__main__":
    logger.setLevel(10)