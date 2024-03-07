"""

Meritous Example: Store


"""
from meritous.core import Model
from meritous.core.properties import UUID4Property, StrProperty, DateProperty
from meritous.core.serializers import JSONSerializer
from meritous.core.stores import FileStore

from datetime import date

class EventModel(Model):

    _schema = {
        "id"          : UUID4Property(),
        "title"       : StrProperty(),
        "date"        : DateProperty(),
        "description" : StrProperty(),
    }


filestore = FileStore(model=EventModel, serializer=JSONSerializer)
event = filestore.load('samples/event.json')
print(event.id)

filestore.save('/tmp/event.json', event)
print('`cat /tmp/event.json`')