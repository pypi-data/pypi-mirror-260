import pytest

import data

import meritous.core.properties

def test_str_property():
    p = meritous.core.properties.StrProperty()
    assert p.type == str
    assert p.validate(data.TEST_STR) == True

def test_str_default():
    p = meritous.core.properties.StrProperty(default=data.TEST_STR)
    assert p.default == data.TEST_STR

def test_str_required():
    p = meritous.core.properties.StrProperty(required=True)
    assert p.is_required == True