"""
Test: Version

Version: 1.1.0
Date updated: 23/11/2023 (dd/mm/yyyy)
"""


# Library
###########################################################################
import pytest

from absfuyu.version import Bumper, ReleaseLevel, ReleaseOption, Version


# Test
###########################################################################
@pytest.fixture
def ver1() -> Bumper:
    """1.0.0"""
    return Bumper(1, 0, 0, ReleaseLevel.FINAL, 0)

@pytest.fixture
def ver132() -> Bumper:
    """1.3.2"""
    return Bumper(1, 3, 2, ReleaseLevel.FINAL, 0)

@pytest.fixture
def ver246rc() -> Bumper:
    """2.4.6.rc0"""
    return Bumper(2, 4, 6, ReleaseLevel.RC, 0)

@pytest.fixture
def ver246dev() -> Bumper:
    """2.4.6.dev0"""
    return Bumper(2, 4, 6, ReleaseLevel.DEV, 0)


# Version
def test_from_tuple():
    try:
        _ = Version.from_tuple((1, 0, 0))
        assert True
    except:
        assert False

def test_from_tuple_2():
    try:
        _ = Version.from_tuple((1, 0, 0, "dev", 0))
        assert True
    except:
        assert False

def test_from_tuple_3():
    try:
        _ = Version.from_tuple((1, 0))
    except:
        assert True


# 1.0.0
def test_100_pf(ver1: Bumper):
    """patch final"""
    ver1.bump(
        option=ReleaseOption.PATCH,
        channel=ReleaseLevel.FINAL
    )
    assert str(ver1) == "1.0.1"

def test_100_mnf(ver1: Bumper):
    """minor final"""
    ver1.bump(
        option=ReleaseOption.MINOR,
        channel=ReleaseLevel.FINAL
    )
    assert str(ver1) == "1.1.0"

def test_100_mjf(ver1: Bumper):
    """major final"""
    ver1.bump(
        option=ReleaseOption.MAJOR,
        channel=ReleaseLevel.FINAL
    )
    assert str(ver1) == "2.0.0"

def test_100_prc(ver1: Bumper):
    """patch rc"""
    ver1.bump(
        option=ReleaseOption.PATCH,
        channel=ReleaseLevel.RC
    )
    assert str(ver1) == "1.0.1.rc0"

def test_100_mnrc(ver1: Bumper):
    """minor rc"""
    ver1.bump(
        option=ReleaseOption.MINOR,
        channel=ReleaseLevel.RC
    )
    assert str(ver1) == "1.1.0.rc0"

def test_100_mjrc(ver1: Bumper):
    """major rc"""
    ver1.bump(
        option=ReleaseOption.MAJOR,
        channel=ReleaseLevel.RC
    )
    assert str(ver1) == "2.0.0.rc0"

def test_100_pd(ver1: Bumper):
    """patch dev"""
    ver1.bump(
        option=ReleaseOption.PATCH,
        channel=ReleaseLevel.DEV
    )
    assert str(ver1) == "1.0.1.dev0"

def test_100_mnd(ver1: Bumper):
    """minor dev"""
    ver1.bump(
        option=ReleaseOption.MINOR,
        channel=ReleaseLevel.DEV
    )
    assert str(ver1) == "1.1.0.dev0"

def test_100_mjd(ver1: Bumper):
    """major dev"""
    ver1.bump(
        option=ReleaseOption.MAJOR,
        channel=ReleaseLevel.DEV
    )
    assert str(ver1) == "2.0.0.dev0"


# 1.3.2
def test_132_pf(ver132: Bumper):
    """patch final"""
    ver132.bump(
        option=ReleaseOption.PATCH,
        channel=ReleaseLevel.FINAL
    )
    assert str(ver132) == "1.3.3"

def test_132_mnf(ver132: Bumper):
    """minor final"""
    ver132.bump(
        option=ReleaseOption.MINOR,
        channel=ReleaseLevel.FINAL
    )
    assert str(ver132) == "1.4.0"

def test_132_mjf(ver132: Bumper):
    """major final"""
    ver132.bump(
        option=ReleaseOption.MAJOR,
        channel=ReleaseLevel.FINAL
    )
    assert str(ver132) == "2.0.0"

def test_132_prc(ver132: Bumper):
    """patch rc"""
    ver132.bump(
        option=ReleaseOption.PATCH,
        channel=ReleaseLevel.RC
    )
    assert str(ver132) == "1.3.3.rc0"

def test_132_mnrc(ver132: Bumper):
    """minor rc"""
    ver132.bump(
        option=ReleaseOption.MINOR,
        channel=ReleaseLevel.RC
    )
    assert str(ver132) == "1.4.0.rc0"

def test_132_mjrc(ver132: Bumper):
    """major rc"""
    ver132.bump(
        option=ReleaseOption.MAJOR,
        channel=ReleaseLevel.RC
    )
    assert str(ver132) == "2.0.0.rc0"

def test_132_pd(ver132: Bumper):
    """patch dev"""
    ver132.bump(
        option=ReleaseOption.PATCH,
        channel=ReleaseLevel.DEV
    )
    assert str(ver132) == "1.3.3.dev0"

def test_132_mnd(ver132: Bumper):
    """minor dev"""
    ver132.bump(
        option=ReleaseOption.MINOR,
        channel=ReleaseLevel.DEV
    )
    assert str(ver132) == "1.4.0.dev0"

def test_132_mjd(ver132: Bumper):
    """major dev"""
    ver132.bump(
        option=ReleaseOption.MAJOR,
        channel=ReleaseLevel.DEV
    )
    assert str(ver132) == "2.0.0.dev0"


# 2.4.6.rc0
def test_246rc_pf(ver246rc: Bumper):
    """patch final"""
    ver246rc.bump(
        option=ReleaseOption.PATCH,
        channel=ReleaseLevel.FINAL
    )
    assert str(ver246rc) == "2.4.6"

def test_246rc_mnf(ver246rc: Bumper):
    """minor final"""
    ver246rc.bump(
        option=ReleaseOption.MINOR,
        channel=ReleaseLevel.FINAL
    )
    assert str(ver246rc) == "2.4.6"

def test_246rc_mjf(ver246rc: Bumper):
    """major final"""
    ver246rc.bump(
        option=ReleaseOption.MAJOR,
        channel=ReleaseLevel.FINAL
    )
    assert str(ver246rc) == "2.4.6"

def test_246rc_prc(ver246rc: Bumper):
    """patch rc"""
    ver246rc.bump(
        option=ReleaseOption.PATCH,
        channel=ReleaseLevel.RC
    )
    assert str(ver246rc) == "2.4.6.rc1"

def test_246rc_mnrc(ver246rc: Bumper):
    """minor rc"""
    ver246rc.bump(
        option=ReleaseOption.MINOR,
        channel=ReleaseLevel.RC
    )
    assert str(ver246rc) == "2.4.6.rc1"

def test_246rc_mjrc(ver246rc: Bumper):
    """major rc"""
    ver246rc.bump(
        option=ReleaseOption.MAJOR,
        channel=ReleaseLevel.RC
    )
    assert str(ver246rc) == "2.4.6.rc1"

def test_246rc_pd(ver246rc: Bumper):
    """patch dev"""
    ver246rc.bump(
        option=ReleaseOption.PATCH,
        channel=ReleaseLevel.DEV
    )
    assert str(ver246rc) == "2.4.7.dev0"

def test_246rc_mnd(ver246rc: Bumper):
    """minor dev"""
    ver246rc.bump(
        option=ReleaseOption.MINOR,
        channel=ReleaseLevel.DEV
    )
    assert str(ver246rc) == "2.5.0.dev0"

def test_246rc_mjd(ver246rc: Bumper):
    """major dev"""
    ver246rc.bump(
        option=ReleaseOption.MAJOR,
        channel=ReleaseLevel.DEV
    )
    assert str(ver246rc) == "3.0.0.dev0"


# 2.4.6.dev0
def test_246dev_pf(ver246dev: Bumper):
    """patch final"""
    ver246dev.bump(
        option=ReleaseOption.PATCH,
        channel=ReleaseLevel.FINAL
    )
    assert str(ver246dev) == "2.4.6"

def test_246dev_mnf(ver246dev: Bumper):
    """minor final"""
    ver246dev.bump(
        option=ReleaseOption.MINOR,
        channel=ReleaseLevel.FINAL
    )
    assert str(ver246dev) == "2.4.6"

def test_246dev_mjf(ver246dev: Bumper):
    """major final"""
    ver246dev.bump(
        option=ReleaseOption.MAJOR,
        channel=ReleaseLevel.FINAL
    )
    assert str(ver246dev) == "2.4.6"

def test_246dev_prc(ver246dev: Bumper):
    """patch rc"""
    ver246dev.bump(
        option=ReleaseOption.PATCH,
        channel=ReleaseLevel.RC
    )
    assert str(ver246dev) == "2.4.6.rc0"

def test_246dev_mnrc(ver246dev: Bumper):
    """minor rc"""
    ver246dev.bump(
        option=ReleaseOption.MINOR,
        channel=ReleaseLevel.RC
    )
    assert str(ver246dev) == "2.4.6.rc0"

def test_246dev_mjrc(ver246dev: Bumper):
    """major rc"""
    ver246dev.bump(
        option=ReleaseOption.MAJOR,
        channel=ReleaseLevel.RC
    )
    assert str(ver246dev) == "2.4.6.rc0"

def test_246dev_pd(ver246dev: Bumper):
    """patch dev"""
    ver246dev.bump(
        option=ReleaseOption.PATCH,
        channel=ReleaseLevel.DEV
    )
    assert str(ver246dev) == "2.4.6.dev1"

def test_246dev_mnd(ver246dev: Bumper):
    """minor dev"""
    ver246dev.bump(
        option=ReleaseOption.MINOR,
        channel=ReleaseLevel.DEV
    )
    assert str(ver246dev) == "2.4.6.dev1"

def test_246dev_mjd(ver246dev: Bumper):
    """major dev"""
    ver246dev.bump(
        option=ReleaseOption.MAJOR,
        channel=ReleaseLevel.DEV
    )
    assert str(ver246dev) == "2.4.6.dev1"