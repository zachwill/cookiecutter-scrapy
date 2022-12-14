"""
Save ModelItem's to a local SQLite database.
"""

from collections import defaultdict

from peewee import chunked

from {{cookiecutter.repo_name}}.items import ModelItem


class ModelPipeline(object):
    "The pipeline stores scraped data in a database."

    def open_spider(self, spider):
        self.models = defaultdict(list)

    def close_spider(self, spider):
        if len(self.models):
            for model_name, list_of_models in self.models.items():
                model = list_of_models[0].model
                for batch in chunked(list_of_models, 25):
                    model.insert_many(batch).on_conflict_replace().execute()

    def process_item(self, item, spider):
        if isinstance(item, ModelItem):
            model_name = type(item)
            self.models[model_name].append(item)
        return item

