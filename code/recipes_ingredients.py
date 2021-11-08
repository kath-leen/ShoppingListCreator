from dataclasses import dataclass

import database


@dataclass
class RecipeIngredientData:
    recipe_id: int
    ingredient_id: int
    quantity: float


class RecipesIngredients:
    def __init__(self, db_filename):
        self.database = database.DatabaseWrapper(db_filename)
        self.database.execute('CREATE TABLE IF NOT EXISTS recipes_ingredients ('
                              'recipe_id INTEGER NOT NULL, '
                              'ingredient_id INTEGER NOT NULL, '
                              'quantity REAL NOT NULL DEFAULT 0, '
                              'FOREIGN KEY (recipe_id) REFERENCES recipes (id), '
                              'FOREIGN KEY (ingredient_id) REFERENCES ingredients (id), '
                              'PRIMARY KEY (recipe_id, ingredient_id))')

    def get_database_wrapper(self):
        return self.database

    def add_recipe_ingredient(self, recipe_id, ingredient_id, quantity):
        self.database.execute(
            'INSERT INTO recipes_ingredients (recipe_id, ingredient_id, quantity) VALUES (?, ?, ?)',
            (recipe_id, ingredient_id, quantity)
        )

    def get_recipe_ingredient(self, recipe_id, ingredient_id):
        res = self.database.execute_and_fetch_one(
            'SELECT recipe_id, ingredient_id, quantity '
            'FROM recipes_ingredients '
            'JOIN ingredients '
            '    ON ingredients.id = recipes_ingredients.ingredient_id '
            'WHERE (recipe_id, ingredient_id) = (?, ?)',
            (recipe_id, ingredient_id)
        )
        if res is None:
            raise Exception("No recipe ID " + str(recipe_id) + " and ingredient ID " + str(ingredient_id) +
                            " pair in the database!")
        return RecipeIngredientData(res[0], res[1], res[2])

    def get_recipe_ingredients(self, recipe_id):
        res = self.database.execute_and_fetch(
            'SELECT recipe_id, ingredient_id, quantity '
            'FROM recipes_ingredients '
            'JOIN ingredients '
            '    ON ingredients.id = recipes_ingredients.ingredient_id '
            'WHERE recipe_id = ?',
            (recipe_id,)
        )
        return [RecipeIngredientData(row[0], row[1], row[2]) for row in res]

    def is_ingredient_used_anywhere(self, ingredient_id):
        res = self.database.execute_and_fetch(
            'SELECT recipe_id '
            'FROM recipes_ingredients '
            'JOIN recipes '
            '    ON recipes.id = recipes_ingredients.recipe_id '
            'WHERE ingredient_id = ?',
            (ingredient_id,)
        )
        return len(res) != 0

    def set_quantity(self, recipe_id, ingredient_id, quantity):
        self.database.execute(
            'UPDATE recipes_ingredients SET quantity = ? WHERE (recipe_id, ingredient_id) = (?, ?)',
            (quantity, recipe_id, ingredient_id)
        )

    def delete_ingredient_from_recipe(self, recipe_id, ingredient_id):
        self.database.execute('DELETE FROM recipes_ingredients WHERE (recipe_id, ingredient_id) = (?, ?)',
                              (recipe_id, ingredient_id))

    def delete_recipe(self, recipe_id):
        self.database.execute('DELETE FROM recipes_ingredients WHERE (recipe_id) = (?)', (recipe_id,)) # TODO: test it!