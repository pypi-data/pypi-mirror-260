"""
Test: Converter

Version: 1.1.0
Date updated: 27/11/2023 (dd/mm/yyyy)
"""


# Library
###########################################################################
import pytest

from absfuyu.general.generator import Generator, Charset
from absfuyu.tools.converter import Text2Chemistry, Base64EncodeDecode


# Test
###########################################################################
@pytest.fixture
def instance():
    return Text2Chemistry()


# convert
def test_convert(instance: Text2Chemistry):
    """Unvailable character"""
    assert instance.convert("jump") == []


def test_convert_2(instance: Text2Chemistry):
    """Unvailable character"""
    assert instance.convert("queen") == []


def test_convert_3(instance: Text2Chemistry):
    """Work"""
    assert instance.convert("bakery") != []


# base64
def test_base64_encode():
    test = Base64EncodeDecode.encode("Hello, World!")
    assert test == "SGVsbG8sIFdvcmxkIQ=="


def test_base64_decode():
    test = Base64EncodeDecode.decode("SGVsbG8sIFdvcmxkIQ==")
    assert test == "Hello, World!"


def test_base64():
    """Run multiple times"""
    TIMES = 100
    test = []
    for x in Generator.generate_string(Charset.FULL, times=TIMES):
        encode = Base64EncodeDecode.encode(x)
        test.append(x == Base64EncodeDecode.decode(encode))
    assert all(test)
