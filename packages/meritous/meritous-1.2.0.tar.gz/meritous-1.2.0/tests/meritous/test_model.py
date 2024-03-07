

import pytest

import data

from meritous.core import Model, Schema, Property
import meritous.core.exceptions

class ModelTest(Model):
    _schema = {
        data.TEST_STR : Property(str, data.TEST_STR_ALT)
    }

def test_model_init():
    m = ModelTest()
    assert isinstance(m._schema, Schema)
    assert m.TEST == data.TEST_STR_ALT
    m.TEST = data.TEST_STR
    assert m.TEST == data.TEST_STR
    m = ModelTest(_schema={
        data.TEST_STR : Property(int, data.TEST_INT)
    })
    assert isinstance(m._schema, Schema)
    assert m.TEST == data.TEST_INT

def test_model_init_invalid_schema():
    with pytest.raises(meritous.core.exceptions.ModelException):
        m = ModelTest(_schema=1)

def test_model_invalid_setattr():
    m = ModelTest()
    with pytest.raises(meritous.core.exceptions.PropertyException):
        m.TEST = data.TEST_INT

def test_model_init_with_data():
    m = ModelTest(_data = {data.TEST_STR : data.TEST_STR_ALT})
    assert m.TEST == data.TEST_STR_ALT

def test_model_items():
    m = ModelTest(_data = {data.TEST_STR : data.TEST_STR_ALT})
    assert m.items() == {data.TEST_STR : data.TEST_STR_ALT}.items()


def test_model_get_schema():
    m = ModelTest()
    assert isinstance(m.schema, Schema)

def test_model_validate():
    m = ModelTest()
    m.validate()

def test_model_validate_invalid_value():
    m = ModelTest(_data = {data.TEST_STR : data.TEST_INT})
    with pytest.raises(meritous.core.exceptions.PropertyException):
        m.validate()

def test_model_validate_invalid_property():
    m = ModelTest(_data = {data.TEST_STR_ALT : data.TEST_INT})
    with pytest.raises(meritous.core.exceptions.ModelException):
        m.validate()
    
def test_model_new():
    m = ModelTest.new({data.TEST_STR : data.TEST_STR_ALT})
    assert m.TEST == data.TEST_STR_ALT