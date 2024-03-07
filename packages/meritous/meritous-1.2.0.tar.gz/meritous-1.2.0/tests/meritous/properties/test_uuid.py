import pytest
import uuid

import meritous.core.properties

def test_uuid_generation():
    p = meritous.core.properties.UUID4Property()
    assert p.type == str
    uuid.UUID(p.default, version=4)

def test_uuid_failed_validation():
    p = meritous.core.properties.UUID4Property()
    assert p.validate('1234') == False
    assert p.validate(1234) == False