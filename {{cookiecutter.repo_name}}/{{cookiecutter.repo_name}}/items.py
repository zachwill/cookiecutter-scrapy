"""
See documentation:  http://doc.scrapy.org/en/latest/topics/items.html
"""

import copy

import moment
from scrapy import Item, Field
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst

from {{cookiecutter.repo_name}} import models


# ----------------------------------------------------------------------------
# Processors
# ----------------------------------------------------------------------------

def strip_whitespace(text):
    text = str(text).replace("\n", " ").replace("\r", " ").strip()
    if text == "":
        return None
    return text


def title_check(text):
    return str(text).title()


def unix_time_to_date(text):
    try:
        date = moment.unix(int(text)).strftime("%Y-%m-%d")
    except:
        date = text
    return date


# ----------------------------------------------------------------------------
# Utilities
# ----------------------------------------------------------------------------

class DefaultLoader(ItemLoader):
    default_input_processor = MapCompose(strip_whitespace)
    default_output_processor = TakeFirst()


class ModelItem(Item):
    """
    Make Peewee models easily turn into Scrapy Items.

    >>> from models import Player
    >>> item = ModelItem(Player())
    """

    def __init__(self, model=None, **kwds):
        super(ModelItem, self).__init__()

        if model:
            self.__model__ = model

        if "Meta" in dir(self):
            for key, processor in self.Meta.__dict__.items():
                if not key.startswith("__"):
                    kwds[key] = processor

        for key in self.model._meta.fields.keys():
            self.fields[key] = Field()

        if kwds is not None:
            for key, processor in kwds.items():
                self.fields[key] = Field(input_processor=MapCompose(
                    strip_whitespace, processor
                ))

    def __setitem__(self, key, value):
        if key not in self.fields:
            self.fields[key] = Field()
        self._values[key] = value

    def copy(self):
        return copy.deepcopy(self)

    def save(self):
        return self.model.from_scrapy_item(self)

    @property
    def model(self):
        return self.__model__


# ----------------------------------------------------------------------------
# Items
# ----------------------------------------------------------------------------

class City(ModelItem):
    __model__ = models.City

    class Meta:
        name = title_check


class Restaurant(ModelItem):
    __model__ = models.Restaurant
