

import pytest

import data

from meritous.core import Schema, Property
import meritous.core.exceptions

def test_schema_init():
    s = Schema(**{})


def test_schema_invalid_property():
    with pytest.raises(meritous.core.exceptions.SchemaException):
        s = Schema(**{ data.TEST_STR : data.TEST_INT })


def test_schema_add_name():
     s = Schema({
          data.TEST_STR : Property(str)
     })
     assert s[data.TEST_STR].name == data.TEST_STR

