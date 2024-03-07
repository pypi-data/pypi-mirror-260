
from meritous.core import Property

import uuid
import datetime


class StrProperty(Property):

    def __init__(self, **kwargs):
        super().__init__(str, **kwargs)


class UUID4Property(Property):

    def __init__(self, required=True):
        default = str(uuid.uuid4())
        super().__init__(str, required=required, default=default)

    def validate(self, value):
        if not super().validate(value):
            return False
        try:
            uuid_obj = uuid.UUID(value, version=4)
        except ValueError:
            return False
        return True


class DateProperty(Property):

    def __init__(self, **kwargs):
        super().__init__(datetime.date, **kwargs)

    def serialize(self, value):
        return str(value)
    
    def deserialize(self, value):
        return self._type.fromisoformat(value)


class IntProperty(Property):

    def __init__(self, **kwargs):
        super().__init__(int, **kwargs)
