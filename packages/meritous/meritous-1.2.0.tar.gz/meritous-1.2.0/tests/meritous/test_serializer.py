import pytest

import data

from meritous.core import Serializer, Property, Model
import meritous.core.exceptions

class ModelTest(Model):
    _schema = {
        data.TEST_STR : Property(str, data.TEST_STR_ALT)
    }
    

def test_serializer_serialize():
    s = Serializer()
    m = ModelTest()
    assert s.serialize(m) == { data.TEST_STR : data.TEST_STR_ALT }

def test_serializer_deserialize():
    s = Serializer()
    m = s.deserialize({ data.TEST_STR : data.TEST_STR_ALT }, ModelTest())
    assert m.TEST == data.TEST_STR_ALT

def test_serializer_deserialize_invalid_data():
    s = Serializer()
    with pytest.raises(meritous.core.exceptions.SerializerException):
        s.deserialize({ data.TEST_STR_ALT : data.TEST_STR_ALT }, ModelTest())