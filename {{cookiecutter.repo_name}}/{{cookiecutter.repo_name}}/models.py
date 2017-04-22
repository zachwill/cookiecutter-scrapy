# -*- coding: utf-8 -*-

"""
Models to store scraped data in a database.
"""

import inspect

from peewee import SqliteDatabase, Model
from peewee import CompositeKey, FloatField, IntegerField, TextField


db = SqliteDatabase("{{cookiecutter.database}}.db", threadlocals=True)


class BaseModel(Model):
    class Meta:
        database = db

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def __delitem__(self, key):
        return setattr(self, key, None)

    @classmethod
    def primary_keys(cls):
        pk = cls._meta.primary_key
        if "field_names" in pk.__dict__:
            names = pk.field_names
        else:
            names = (pk.name, )
        return names

    @classmethod
    def from_scrapy_item(cls, item):
        with db.atomic():
            lookup = {}
            for key in cls.primary_keys():
                lookup[key] = item[key]

            cls_model, created = cls.get_or_create(**lookup)
            for key, value in item.iteritems():
                setattr(cls_model, key, value)

            return cls_model.save()


# ----------------------------------------------------------------------------
# Example Models
# ----------------------------------------------------------------------------

class City(BaseModel):
    name = TextField()
    state = TextField()

    class Meta:
        db_table = "cities"
        indexes = [(("name", "state"), True)]
        primary_key = CompositeKey("name", "state")


class Restaurant(BaseModel):
    name = TextField()

    class Meta:
        db_table = "restaurants"


# ----------------------------------------------------------------------------
# Automatically create the tables...
# ----------------------------------------------------------------------------

def create_tables():
    models = []
    for name, cls in globals().items():
        if inspect.isclass(cls) and issubclass(cls, BaseModel):
            if name == "BaseModel":
                continue
            models.append(cls)
    db.create_tables(models, safe=True)


if __name__ == "__main__":
    create_tables()
