__author__ = 'elon'

import collections.abc

def single_input_handler(input):
    if not isinstance(input, str) and isinstance(input, collections.abc.Iterable):
        for i in input:
            yield i
    else:
        yield input


def all_inputs_handler(input):
    yield single_input_handler(input)


def single_ingredient_handler(ingr):
    if not isinstance(ingr, str) and isinstance(ingr, collections.abc.Iterable):
        for i in ingr:
            yield i
        while True:
            yield i
    else:
        while True:
            yield ingr


def all_ingredients_handler(ingr):
    while True:
        yield single_ingredient_handler(ingr)


class BaseRecipe(object):
    input_handler = staticmethod(single_input_handler)
    ingredient_handlers = {}

    def __init__(self, **kwargs):
        self.kwargs = {key: self._get_ingredient_handler(key)(value)
                       for key, value in kwargs.items()}
        self.input = None

        self.init()

    def init(self):
        pass

    def _get_ingredient_handler(self, ingredient):
        try:
            return self.ingredient_handlers[ingredient]
        except KeyError:
            return single_ingredient_handler

    def cook(self, input=None):
        for i in self.input_handler(input):
            kwargs = {key: next(value) for key, value in self.kwargs.items()}

            for j in self.run(i, **kwargs):
                yield j


def start_and_print_results(iter):
    for result in iter:
        print(result)
