import pytest

import data

from meritous.core import Store, Serializer, Property, Model
import meritous.core.exceptions

class ModelTest(Model):
    _schema = {
        data.TEST_STR : Property(str, data.TEST_STR_ALT)
    }
    

def test_store_load():
    s = Store(ModelTest, Serializer)
    m = s.load({ data.TEST_STR : data.TEST_STR_ALT })
    assert m.TEST == data.TEST_STR_ALT

def test_store_save():
    m = ModelTest()
    s = Store(ModelTest, Serializer)
    assert s.save(m) == { data.TEST_STR : data.TEST_STR_ALT }