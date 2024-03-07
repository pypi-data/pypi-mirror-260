Getting Started
======================================

At it's heart, Meritous is incredibly, perhaps absurdly, simple to use. Define a set of properties as a schema for your model and begin to use the model as you would any other Python class.

Basic Usage
-----------

Meritous can be used to quickly bootstrap simple Models with defined data elements. The following example demonstrates the basic functionality in the context of an "Event" data structure.

.. code-block:: python

  from meritous import Model
  from meritous.properties import UUIDProperty, StrProperty, DateProperty

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

Models and they data are intended to be operated as Python data types in the usual ways. Meritous then defines a simple way to map Model data into a storage representations, which are intentionally not part of the core package, for saving into a data store or for onward transportation. For example, you might transform a model into JSON for transport or use a DynamoDB transform to store the data in the cloud.
