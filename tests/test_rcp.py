from unittest import TestCase

from recipe.rcp import BaseRecipe

__author__ = 'elon'


class AddString(BaseRecipe):
    def run(self, input, a, b):
        yield a + input + b
        yield b + input + a
        yield input + a + b


class TestRcp(TestCase):
    def setUp(self):
        self.addstringrecipe = AddString(a='1', b='2')

    def test_cook(self):
        b = self.addstringrecipe.cook(['foo', 'bar', 'baz'])

        self.assertEqual(list(b), ['1foo2', '2foo1', 'foo12', '1bar2', '2bar1', 'bar12', '1baz2', '2baz1', 'baz12'])

    def test_recipes(self):
        pass
        # recipes.test.addstring
