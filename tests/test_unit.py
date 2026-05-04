import pytest
from app.services.logic import get_package_limit


def test_free_package_limit():
    assert get_package_limit("FREE") == 2

def test_pro_package_limit():
    assert get_package_limit("PRO") == 100

def test_unknown_package_limit():
    assert get_package_limit("GOLD") == 0