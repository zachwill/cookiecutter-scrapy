# -*- coding: utf-8 -*-

"""
Save ModelItem's to a local SQLite database.
"""

from {{cookiecutter.repo_name}}.items import ModelItem


class ModelPipeline(object):
    "The pipeline stores scraped data in a database."

    def process_item(self, item, spider):
        if isinstance(item, ModelItem):
            item.save()
        return item
