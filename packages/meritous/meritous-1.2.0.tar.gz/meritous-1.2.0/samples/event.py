"""

Meritous Example: Event Model


"""
from meritous.core import Model
from meritous.core.properties import UUID4Property, StrProperty, DateProperty
from meritous.core.serializers import JSONSerializer

from datetime import date

class EventModel(Model):

    _schema = {
        "id"          : UUID4Property(),
        "title"       : StrProperty(),
        "date"        : DateProperty(),
        "description" : StrProperty(),
    }


event = EventModel()
event.title = 'Sample Event'
event.date = date.fromisoformat('2023-01-10')
print(event.id)
print(event.title)
print(event.date)
print(event._schema['title'].name)

serializer = JSONSerializer()
print(serializer.serialize(event))

