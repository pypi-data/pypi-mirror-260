import datetime

import data

import meritous.core.properties

def test_date_property():
    p = meritous.core.properties.DateProperty()
    assert p.type == datetime.date
    assert p.validate(datetime.date.fromisoformat('2023-01-10')) == True

def test_date_default():
    p = meritous.core.properties.DateProperty(default=datetime.date.fromisoformat('2023-01-10'))
    assert p.default == datetime.date.fromisoformat('2023-01-10')

def test_date_required():
    p = meritous.core.properties.DateProperty(required=True)
    assert p.is_required == True

def test_date_serialize():
    p = meritous.core.properties.DateProperty()
    assert p.serialize(datetime.date.fromisoformat('2023-01-10')) == '2023-01-10'

def test_date_deserialize():
    p = meritous.core.properties.DateProperty()
    v = p.deserialize('2023-01-10') 
    assert type(v) == datetime.date
    assert type(v) == p.type