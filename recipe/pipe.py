import recipe.rcp

__author__ = 'elon'


class Pipe(recipe.rcp.BaseRecipe):
    input_handler = staticmethod(recipe.rcp.all_inputs_handler)
    ingredient_handlers = {'items': recipe.rcp.all_inputs_handler}

    def run(self, input, items):
        output = input
        for i in items:
            output = i.cook(output)

        for i in output:
            yield i
