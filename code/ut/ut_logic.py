import recipes
import ingredients
import recipes_ingredients
import logic
from ut_base import Ut


class UtLogic(Ut):
    def __init__(self, db_filename):
        self.recipes = recipes.Recipes(db_filename)
        self.ingredients = ingredients.Ingredients(db_filename)
        self.recipes_ingredients = recipes_ingredients.RecipesIngredients(db_filename)
        self.recipes_data = [recipes.Recipe(0, 'scrambled eggs', 'break eggs, mix them with milk and fry'),
                             recipes.Recipe(1, 'cappuccino',      'prepare coffee, foam the milk, add to the coffee')]
        self.ingredients_data = [ingredients.Ingredient(0, 'eggs',   'pieces'),
                                 ingredients.Ingredient(1, 'milk',   'litres'),
                                 ingredients.Ingredient(2, 'coffee', 'grams')]
        self.recipes_ingredients_quantity = {self.recipes_data[0].name: {self.ingredients_data[0].name: 5,
                                                                         self.ingredients_data[1].name: 0.2},
                                             self.recipes_data[1].name: {self.ingredients_data[1].name: 0.1,
                                                                         self.ingredients_data[2].name: 50}}
        self.ingredient_sum_quantity = self.calculate_sum_quantity()
        self.add_all_recipes()
        self.add_all_ingredients()
        self.add_all_recipes_ingredients()

    def add_all_recipes(self):
        for i in range(len(self.recipes_data)):
            self.recipes.add_recipe(self.recipes_data[i].name, self.recipes_data[i].text)
            rec = self.recipes.get_recipe_by_name(self.recipes_data[i].name)
            self.recipes_data[i].recipe_id = rec.recipe_id

    def add_all_ingredients(self):
        for i in range(len(self.ingredients_data)):
            self.ingredients.add_ingredient(self.ingredients_data[i].name, self.ingredients_data[i].meas_unit)
            ingr = self.ingredients.get_ingredient_by_name(self.ingredients_data[i].name)
            self.ingredients_data[i].ingredient_id = ingr.ingredient_id

    def add_all_recipes_ingredients(self):
        for recipe_name in self.recipes_ingredients_quantity.keys():
            for ingredient_name in self.recipes_ingredients_quantity.get(recipe_name).keys():
                recipe_id = self.recipes.get_recipe_by_name(recipe_name).recipe_id
                ingredient_id = self.ingredients.get_ingredient_by_name(ingredient_name).ingredient_id
                self.recipes_ingredients.add_recipe_ingredient(recipe_id, ingredient_id,
                                                               self.recipes_ingredients_quantity
                                                               [recipe_name][ingredient_name])

    def calculate_sum_quantity(self):
        ingr_sum_quantity = {}
        for recipe_name in self.recipes_ingredients_quantity.keys():
            for ingredient_name in self.recipes_ingredients_quantity.get(recipe_name).keys():
                ingr_sum_quantity[ingredient_name] = ingr_sum_quantity.get(ingredient_name, 0) + \
                                                     self.recipes_ingredients_quantity[recipe_name][ingredient_name]
        return ingr_sum_quantity

    def check_summarize_all_ingredients(self):
        desired_recipes_by_id = [rec.recipe_id for rec in self.recipes_data]
        ingredients_summary_data = logic.summarize_all_ingredients(desired_recipes_by_id, self.recipes_ingredients)
        for ingredient_id in ingredients_summary_data.keys():
            ingredient_name = self.ingredients.get_ingredient_by_id(ingredient_id).name
            self.check_equal(ingredients_summary_data[ingredient_id], self.ingredient_sum_quantity[ingredient_name])


    def check(self):
        self.check_summarize_all_ingredients()