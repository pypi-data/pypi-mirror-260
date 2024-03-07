from meritous.core import Serializer
from .exceptions import SerializerException

import json
import toml

class JSONSerializer(Serializer):

    def serialize(self, model):
        return json.dumps(super().serialize(model))
    
    def deserialize(self, data, model):
        return super().deserialize(json.loads(data), model)
    
class TOMLSerializer(Serializer):

    def serialize(self, model):
        return toml.dumps(super().serialize(model))
    
    def deserialize(self, data, model):
        return super().deserialize(toml.loads(data), model)