Meritous provides simple Python Models
======================================

Meritous is an absurdly simply approach to "Models" in Python. It came about because there is no modern, framework agnostic approach to modelling data.

On the face of it the usage is very trivial; but the intent is that Meritous is a building block for more complex data models. Essentially, it provides a simple Model class which can contain data to be used in Python applications. It then sets out a standard practice for transforming that data for storage or transport.

.. _installation:

Installation
------------

To use Meritous, first install it using pip:

.. code-block:: console

   (.venv) $ pip install meritous

Sample Usage
------------

Here is an example demonstrating a full use case for Meritous (utilising optional integrations for AWS DynamoDB).

.. code-block:: python

  from meritous import Model
  from meritous.properties import UUIDProperty, StrProperty, DateProperty

  from meritous.aws.stores.dynamodb import DynamoDBStore

  import boto3, datetime

  class EventModel(Model):

      _schema = {
          "id"    : UUIDProperty(),
          "title" : StrProperty(),
          "date"  : DateProperty()
      }


  event = Event()
  event.title = 'Sample Event'
  event.date = datetime.date.fromisoformat('2023-01-10')

  dynamodb = boto3.resource('dynamodb')

  store = DynamoDBStore(dynamodb.Table('sample_event_table'))

  store.save(KeyProperties=['id'], Item=event)

  event_recover = store.get(Key={'id' : event.id}, Model=EventModel)

  print(event.id == event_recover.id)



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   Home <self>
   start
   concepts
   properties
   stores
   extensions
