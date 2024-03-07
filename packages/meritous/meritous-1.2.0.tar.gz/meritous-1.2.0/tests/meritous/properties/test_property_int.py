import data

import meritous.core.properties

def test_int_property():
    p = meritous.core.properties.IntProperty()
    assert p.type == int
    assert p.validate(data.TEST_INT) == True

def test_int_default():
    p = meritous.core.properties.IntProperty(default=data.TEST_INT)
    assert p.default == data.TEST_INT

def test_int_required():
    p = meritous.core.properties.IntProperty(required=True)
    assert p.is_required == True