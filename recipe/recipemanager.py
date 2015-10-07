__author__ = 'elon'

import importlib

class RecipeManager:
    def __init__(self, namespace='recipes'):
        self.namespace = namespace

    def __getattr__(self, key):
        module = importlib.import_module(self.namespace + '.' + key)
        try:
            return module.Recipe
        except AttributeError:
            return RecipeManager(self.namespace + '.' + key)