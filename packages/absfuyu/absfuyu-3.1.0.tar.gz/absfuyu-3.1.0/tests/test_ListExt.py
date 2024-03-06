"""
Test: ListExt

Version: 1.2.0
Date updated: 25/12/2023 (dd/mm/yyyy)
"""


# Library
###########################################################################
import pytest

from absfuyu.general.data_extension import ListExt


# Test
###########################################################################
@pytest.fixture
def example():
    return ListExt([
        3, 8, 5,
        "Test", "String", "ABC",
        [1,2,3], [0,8,6]
    ])

@pytest.fixture
def example_2():
    return ListExt([
        "Test", "String", "ABC",
        "Tension", "Tent", "Strong"
    ])


# stringify
def test_stringify(example: ListExt):
    assert all([isinstance(x, str) for x in example.stringify()]) is True


# sorts
def test_sorts(example: ListExt):
    assert example.sorts() == [3, 5, 8, 'ABC', 'String', 'Test', [0, 8, 6], [1, 2, 3]]


# freq
def test_freq(example_2: ListExt):
    assert example_2.freq(sort=True) == {'ABC': 1, 'String': 1, 'Strong': 1, 'Tension': 1, 'Tent': 1, 'Test': 1}

def test_freq_2(example_2: ListExt):
    assert example_2.freq(sort=True, num_of_first_char=2) == {'AB': 1, 'St': 2, 'Te': 3}

def test_freq_3(example_2: ListExt):
    assert example_2.freq(sort=True, num_of_first_char=2, appear_increment=True) == [1, 3, 6]


# slice_points
def test_slice_points(example_2: ListExt):
    assert example_2.slice_points([1, 3]) == [['Test'], ['String', 'ABC'], ['Tension', 'Tent', 'Strong']]


# pick_one
def test_pick_one():
    """Empty list"""
    try:
        ListExt([]).pick_one()
    except:
        assert True

def test_pick_one_2(example_2: ListExt):
    assert len([example_2.pick_one()]) == 1


# len_items
def test_len_items(example_2: ListExt):
    assert example_2.len_items() == [4, 6, 3, 7, 4, 6]


# mean_len
def test_mean_len(example_2: ListExt):
    assert example_2.mean_len() == 5.0


# apply
def test_apply(example: ListExt):
    assert example.apply(str) == example.stringify()


# unique
def test_unique():
    assert ListExt([1, 1, 1, 1]).unique() == [1]


# head
def test_head(example: ListExt):
    assert example.head(3) == [3, 8, 5]

def test_head_2(example: ListExt):
    """Max head len"""
    assert example.head(100) == list(example)


# tail
def test_tail(example_2: ListExt):
    assert example_2.tail(2) == ["Tent", "Strong"]

def test_tail_2(example_2: ListExt):
    assert example_2.tail(100) == list(example_2)


# get_random
def test_get_random(example_2: ListExt):
    test = example_2.get_random(20)
    assert len(test) == 20


# flatten
def test_flatten(example: ListExt):
    test = example.flatten()
    assert test