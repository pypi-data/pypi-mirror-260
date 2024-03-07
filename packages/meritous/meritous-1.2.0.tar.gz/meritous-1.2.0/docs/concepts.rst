Core Concepts
======================================

There are only four main concepts in Meritous:

* Model
    The main data structure containing a Schema of defined Properties
* Schema
    Represents the expected data structure of a Model
* Property
    The main data values of the Model referenced in a Schema
* Store
    Stores are used to transform models for storage or transport


Models
------

Models represent the main data structure of Meritous.

.. autoclass :: meritous.core::Model
  :members:
  :special-members: __setattr__, __getattr__

In-line Models
^^^^^^^^^^^^^^

An alternative way to make use of Models is in-line using the class constructor. Because there is no special notation or metadata associated with Models other than a schema (in the form of a dictionary) there is no explicit need to declare your own class other than convention or convenience.

.. code-block:: python

   from meritous import Model
   from meritous.core import Property

   mymodel = Model({
      'property' : Property(str)
   })
