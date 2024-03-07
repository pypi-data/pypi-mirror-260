Properties
======================================

Properties are the data primitives of Meritous. Several are included as built-in and you can quickly and easily define your own as well.

Built-in Properties
-------------------

.. autoclass:: meritous.properties::StrProperty

.. autoclass:: meritous.properties::IntProperty

.. autoclass:: meritous.properties::UUID4Property

Creating additional Properties
------------------------------

Properties are created simply by sub-classing Property. For example, imagine we wanted a Property representing string data (this is one of Meritous' built-in properties):

.. code-block:: python

  from meritous.core import Property

  class StrProperty:
    pass


In itself this isn't very helpful other than giving our Property a special name. However, we can overload the `__init__` method to make this class validate specifically strings:

.. code-block:: python

  from meritous.core import Property

  class StrProperty:

    def __init__(self, **kwargs):
      super().__init__(str, **kwargs)


We can take advantage of 'type' being the only positional argument in the original `Property.__init__` definition to carry any keyword arguments whilst forcing `type` to be str.

This is a very simple property for which the `validate` method will test values against the str type. For example:

.. code-block:: python

  >>> from meritous.properties import StrProperty
  >>> p = StrProperty()
  >>> p.validate('a string')
  'True'
  >>> p.validate(1)
  'False'


There are two other things we might want to do, however, for more complex Properties: set a default value and add additional validation steps.

To set a default is once again managed by over-loading `__init__`. Imagine an example Property (again one of Meritous' built-in options) that handles UUID's.

.. code-block:: python

  from meritous.core import Property

  import uuid

  class UUID4Property(Property):

    def __init__(self, required=True):
      default = str(uuid.uuid4())
      super(Property, self).__init__(uuid.UUID, required=required, default=default)

In this case we didn't use the kwargs hack because for this Property we want more control over the keyword arguments. In this case we will simply proxy one keyword argument (required) and force-set the one that we are interested in (default).

The problem we have now is that UUID4's can be represented in several ways. So the basic functionality of `validate` will work for instances of the UUID class, but you might want to quickly check that some other format of UUID (perhaps as a string or hex) is valid. To do this we can simply overload the `validate` method:

.. code-block:: python

  from meritous.core import Property

  import uuid

  class UUID4Property(Property):

    def __init__(self, required=True):
      default = str(uuid.uuid4())
      super(Property, self).__init__(uuid.UUID, required=required, default=default)

    def validate(self, value):
      if not super(Property, self).validate(value):
        return False
      try:
        uuid_obj = UUID(value, version=4)
      except ValueError:
        return False
      return True

This will now validate several ways.

.. code-block:: python

  >>> from meritous.properties import UUID4Property
  >>> import uuid
  >>> p = UUID4Property()
  >>> str(p.default)
  '0382d829-0fd7-4587-9446-fb7371369e94'
  >>> p.validate(str(p.default))
  'True'
  >>> p.validate(uuid.UUID4())
  'True'
