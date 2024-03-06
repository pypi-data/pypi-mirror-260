"""
Test: DictExt

Version: 1.2.0
Date updated: 01/12/2023 (dd/mm/yyyy)
"""


# Library
###########################################################################
import pytest

from absfuyu.general.data_extension import DictExt


# Test
###########################################################################
@pytest.fixture
def example():
    return DictExt({
        "Line 1": 99,
        "Line 2": 50
    })


# analyze
def test_analyze(example: DictExt):
    assert example.analyze() == {'max_value': 99, 'min_value': 50, 'max': [('Line 1', 99)], 'min': [('Line 2', 50)]}

def test_analyze_2():
    """When values are not int or float"""
    ...


# swap
def test_swap(example: DictExt):
    assert example.swap_items() == {99: 'Line 1', 50: 'Line 2'}


# apply
def test_apply(example: DictExt):
    """Values"""
    assert example.apply(str) == {'Line 1': '99', 'Line 2': '50'}

def test_apply_2():
    """Keys"""
    assert DictExt({1: 1}).apply(str, apply_to_value=False) == {'1': 1}