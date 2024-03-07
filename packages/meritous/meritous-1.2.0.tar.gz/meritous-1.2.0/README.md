[![PyPI](https://img.shields.io/pypi/v/meritous?style=for-the-badge)](https://pypi.org/project/meritous/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/meritous?style=for-the-badge)
![PyPI - License](https://img.shields.io/pypi/l/meritous?style=for-the-badge)
[![Codecov](https://img.shields.io/codecov/c/github/errant/meritous?style=for-the-badge)](https://app.codecov.io/github/errant/meritous)
[![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/errant/meritous?style=for-the-badge)](https://codeclimate.com/github/errant/meritous)

# Meritous


Meritous is an absurdly simply approach to "Models" in Python.

It came about because there is no modern, framework agnostic approach to modelling data.

On the face of it the usage is very trivial; but the intent is that Meritous is a building block for more complex data models. Essentially, it provides a simple Model class which can contain data to be used in Python applications. It then sets out a standard practice for transforming that data for storage or transport.

- [Documentation](https://meritous.readthedocs.io/en/latest/)

## Installation

```bash
pip install meritous
```

## Basic Usage

```python
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
```
