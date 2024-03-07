"""
Simple Python Models
"""
__version__ = "1.2.0"

from .exceptions import *
from .i18n import text


class Property:
    """
    Property is the core element of a Meritous Model and Schema. Each property represents a data element of the Model and is used to validate it's type and content. In general Property should be subclassed and the `validate` method overloaded.

    Parameters
    ----------
    type
        Valid Python type representing the expected type of this property
    default
        The default value for the property
    required
        Indicates weather this property is a required value
    """
    _type = None
    _default = None
    _required = None

    def __init__(self, type, default=None, required=True):
        self._type = type
        self._required = required

        if default and not self.validate(default):
            raise PropertyException(text.error.prop.type.format(self.__class__.__name__, type(default)))

        self._default = default

    def validate(self, value):
        """
        Validate a property against a provided value


        Parameters
        ----------
        value
            Value to be tested against the set Property type
        """
        return type(value) == self._type

    @property
    def is_required(self):
        return self._required

    @property
    def default(self):
        return self._default

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._name
    
    @property 
    def classname(self):
        return self.__class__.__name__

    def _add_name(self, name):
        self._name = name

    def serialize(self, value):
        return self._type(value)
    
    def deserialize(self, value):
        return self._type(value)


class Schema(dict):

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)
        for name in self:
            if not issubclass(self[name].__class__, Property):
                raise SchemaException('Property {0} is not an implementation of meritous.Property'.format(name))
            self[name]._add_name(name)


class Model:
    """
    Models are the main data container in Meritous. For each model you will define a Schema that contains a set of properties,

    The general way you will want to use Models is to subclass them and define the schema (as a dictionary of properties). This gives you a reusable, named Model to represent your data structure in your code.

    .. code-block:: python

      from meritous import Model
      from meritous.core import Property

      class MyModel(Model):

        _schema = {
          'property' : Property(str)
        }

    .. note:: In general you wouldn't reference `Property` directly.


    Parameters
    ----------
    _schema
        Optionally specify the schema in the class constructor to creation of Models in-line (see `In-line Models`_)

    """
    _schema = None
    _data = {}

    def __init__(self, _schema=None, _data=None):
        self._schema = _schema if _schema else self._schema
        if type(self._schema) != dict:
            raise ModelException(text.error.model.schema.format(self.__class__.__name__))
        self._schema = Schema(**self._schema)
        if _data:
            self._data = _data
        else:
            self._data = {name: property.default for name, property in self._schema.items()}

    def __getattr__(self, name):
        """
            Allows access to a Model's properties as a class attribute

            Parameters
            ----------
            name
                Name of attribute to access
        """
        if name in self._data:
            return self._data[name]

    def __setattr__(self, name, value):
        """
            Allows updating of a Model's properties via class attributes (e.g. Model.property_name = "some value")

            Parameters
            ----------
            name
                Name of attribute to update
            value
                Value to update
        """
        if name != '_data' and name in self._data:
            if not self._schema[name].validate(value):
                raise PropertyException(text.error.prop.set.format(self.__class__.__name__, value, self._type, self._schema[name]._type))
            self._data[name] = value
        else:
            self.__dict__[name] = value

    def items(self):
        return self._data.items()
    
    @property
    def schema(self):
        return self._schema
    
    def validate(self):
        for name, value in self._data.items():
            if name not in self._schema:
                raise ModelException(text.error.model.validate.format(name))
            if not self._schema[name].validate(value):
                property = self._schema[name]
                raise PropertyException(text.error.prop.type.format(property.classname, property.type))
        return True
    
    @classmethod
    def new(cls, data):
        return cls(_data=data)


class Serializer:

    def serialize(self, model):
        """
            Serialize a model into a different representation (for storage or transport)

            Parameters
            ----------
            serializer
                The Serialiser object used to marshall the properties of a Model
        """
        return {name: model.schema[name].serialize(value) for name, value in model.items()}

    def deserialize(self, data, model):
        def _deserialize(name, value, model):
            if name not in model.schema:
                raise SerializerException(text.error.serializer.schema.format(name))
            return model.schema[name].deserialize(value)
        return model.new({name: _deserialize(name, value, model) for name, value in data.items()})



class Store:

    def __init__(self, model, serializer):
        self.model = model 
        self.serializer = serializer

    def save(self, model):
        return self.serializer().serialize(model)

    def load(self, data):
        return self.serializer().deserialize(data, self.model())
