"""
Absfuyu: Performance
--------------------
Performance Check

Version: 1.1.0
Date updated: 11/12/2023 (dd/mm/yyyy)

Feature:
--------
- measure_performance
- var_check
- source_this
"""


# Module level
###########################################################################
__all__ = [
    # Wrapper
    "measure_performance",
    # Functions
    "var_check",
    "source_this",
]


# Library
###########################################################################
from functools import wraps as __wraps
from inspect import getsource
from time import perf_counter as __perf_counter
import tracemalloc as __tracemalloc
from typing import Any, Callable, List, Optional, Tuple, Union

from absfuyu.general.data_extension import ListNoDunder


# Function
###########################################################################
def measure_performance(func):
    r"""
    Measure performance of a function

    Usage
    -----
    Use this as the decorator (``@measure_performance``)

    Example:
    --------
    >>> @measure_performance
    >>> def test():
    ...     return 1 + 1
    >>> test()
        ----------------------------------------
        Function: test
        Memory usage:		 0.000000 MB
        Peak memory usage:	 0.000000 MB
        Time elapsed (seconds):	 0.000002
        ----------------------------------------
    """
    
    @__wraps(func)
    def wrapper(*args, **kwargs):
        # Start memory measure
        __tracemalloc.start()
        # Start time measure
        start_time = __perf_counter()
        # Run function
        func(*args, **kwargs)
        # Get memory stats
        current, peak = __tracemalloc.get_traced_memory()
        # Get finished time
        finish_time = __perf_counter()
        # End memory measure
        __tracemalloc.stop()
        
        # Print output
        # print(f'{"-"*40}')
        # print(f'Function: {func.__name__}')
        # #print(f'Method: {func.__doc__}')
        # print(f"Memory usage:\t\t {current / 10**6:.6f} MB")
        # print(f"Peak memory usage:\t {peak / 10**6:.6f} MB")
        # print(f'Time elapsed (seconds):\t {finish_time - start_time:.6f}')
        # print(f'{"-"*40}')
        
        stat = {
            "Function": func.__name__,
            "Memory usage": current / 10**6,
            "Peak memory usage": peak / 10**6,
            "Time elapsed (seconds)": finish_time - start_time,
        }
        out: bool = False
        
        print(f"""
        {"-"*40}
        Function: {stat["Function"]}
        Memory usage:\t\t {stat["Memory usage"]:,.6f} MB
        Peak memory usage:\t {stat["Peak memory usage"]:,.6f} MB
        Time elapsed (seconds):\t {stat["Time elapsed (seconds)"]:,.6f}
        {"-"*40}
        """)
        
        if out:
            return stat
        
    return wrapper


def var_check(variable: Any, full: bool = False):
    """
    Check a variable

    Parameters
    ----------
    variable : Any
        Variable that needed to check

    full : bool
        | ``True``: Shows full detail
        | ``False``: Hides ``dir`` and ``docstring``


    Example:
    --------
    >>> test = "test"
    >>> var_check(test)
    {'value': 'test', 'class': str, 'id': ...}
    """
    
    # Check class
    try:
        clss = [variable.__name__, type(variable)]
    except:
        clss = type(variable)

    output = dict()
    try:
        output = {
            "value": variable,
            "class": clss,
            "id": id(variable),
        }
    except:
        return None

    # Docstring
    try:
        lc = [ # list of Python data types
            str,
            int, float, complex,
            list, tuple, range,
            dict,
            set, frozenset,
            bool,
            bytes, bytearray, memoryview,
            type(None),
        ]
        if type(variable) in lc:
            pass
        else:
            docs = variable.__doc__
            if full:
                output["docstring"] = docs
    except:
        pass

    # Dir
    try:
        if full:
            output["dir"] = ListNoDunder(variable.__dir__())
    except:
        pass

    # Output
    return output


def source_this(function: Callable) -> str:
    """
    Show the source code of a function

    Parameters
    ----------
    function : Callable
        Just put in the function name

    Returns
    -------
    str
        Source code
    """
    return getsource(function)


# Class
###########################################################################
class Checker:
    """Check a variable"""
    def __init__(self, checker: Any) -> None:
        self.item_to_check = checker
    def __str__(self) -> str:
        return self.item_to_check.__str__()
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.item_to_check})"

    @property
    def name(self) -> Union[Any, None]:
        try:
            return self.item_to_check.__name__
        except:
            return None

    @property
    def value(self) -> Any:
        return self.item_to_check

    @property
    def docstring(self) -> Union[str, None]:
        """:returns: ``self.item_to_check.__doc__``"""
        return self.item_to_check.__doc__

    @property
    def class_(self) -> Any:
        return type(self.item_to_check)

    @property
    def id_(self) -> int:
        return id(self.item_to_check)

    @property
    def dir_(self) -> List[str]:
        """:returns: ``dir(self.item_to_check)``"""
        # return self.item_to_check.__dir__()
        return ListNoDunder(self.item_to_check.__dir__())
    
    @property
    def source(self) -> Union[str, None]:
        """:returns: Source code"""
        try:
            return getsource(self.item_to_check)
        except:
            return None

    def check(self, full: bool = False):
        """
        Check
        """
        out = {
            "name": self.name,
            "value": self.value,
            "class": self.class_,
            "id": self.id_,
        }
        if full:
            out["dir"] = self.dir_
            out["docs"] = self.docstring
            out["source"] = self.source
        return out


# Run
###########################################################################
if __name__ == "__main__":
    pass
