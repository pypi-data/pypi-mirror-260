"""

Meritous Example: Serialization


"""
from meritous.core import Model
from meritous.core.properties import UUID4Property, StrProperty, DateProperty
from meritous.core.serializers import JSONSerializer, TOMLSerializer

from datetime import date

class EventModel(Model):

    _schema = {
        "id"          : UUID4Property(),
        "title"       : StrProperty(),
        "date"        : DateProperty(),
        "description" : StrProperty(),
    }


json_data = '{"id": "14992f46-67bd-4a7c-ab22-0209609109", "title": "Sample Event 2", "date": "2023-01-10", "description": "None"}'


event = EventModel()
event.title = 'Sample Event'
event.date = date.fromisoformat('2023-01-10')

print('JSON')
serializer = JSONSerializer()
print(serializer.serialize(event))

print('JSON deserialize')
event_two = serializer.deserialize(json_data, EventModel())
print(event_two.id)

print('TOML')
serializer = TOMLSerializer()
print(serializer.serialize(event))
