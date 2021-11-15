import recipes
import ingredients
import recipes_ingredients
import command_options_parser
import csv
import os
from ut_base import Ut
from dataclasses import dataclass


# TODO: same as in ut_csv_reader, can be combined later
@dataclass
class RecipeIngredientCsvUtData:
    ingredient_name: int
    quantity: float
    ingredient_measure_unit: int


class UtCommandOptionsParser(Ut):
    def __init__(self, db_filename):
        self.ut_file_name_without_extension = 'recipe_ut_csv'
        self.path = '../../csv'
        self.ut_file_full_name = self.path + '/' + self.ut_file_name_without_extension + '.csv'
        self.recipe_ingredient_csv_data_array = [RecipeIngredientCsvUtData('Potato', 0.5, 'grams'),
                                                 RecipeIngredientCsvUtData('carrot', 0.3, 'kilograms')]

        self.cmd_options_parser = command_options_parser.CommandOptionsParser(db_filename)
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
        self.__add_all_recipes()
        self.__add_all_ingredients()
        self.__add_all_recipes_ingredients()

        if os.path.exists(self.ut_file_full_name):
            os.remove(self.ut_file_full_name)
        self.__create_csv_file()

    # TODO: same as in ut_csv_reader and ut_logic, can be combined later
    def __del__(self):
        if os.path.exists(self.ut_file_full_name):
            os.remove(self.ut_file_full_name)

        for recipe_data in self.recipes_data:
            if self.recipes.recipe_exists(recipe_data.name):
                recipe_id = self.recipes.get_recipe_by_name(recipe_data.name).recipe_id
                self.recipes_ingredients.delete_recipe(recipe_id)
                self.recipes.delete_recipe(recipe_id)
        for ingredient_data in self.ingredients_data:
            if self.ingredients.ingredient_exists(ingredient_data.name):
                ingredient_id = self.ingredients.get_ingredient_by_name(ingredient_data.name).ingredient_id
                self.ingredients.delete_ingredient(ingredient_id)

        recipe_name = self.ut_file_name_without_extension
        if self.recipes.recipe_exists(recipe_name):
            recipe_id = self.recipes.get_recipe_by_name(recipe_name).recipe_id
            self.recipes_ingredients.delete_recipe(recipe_id)
            self.recipes.delete_recipe(recipe_id)

        for recipe_ingredient_data in self.recipe_ingredient_csv_data_array:
            if self.ingredients.ingredient_exists(recipe_ingredient_data.ingredient_name.lower()):
                ingredient_id = \
                    self.ingredients.get_ingredient_by_name(
                        recipe_ingredient_data.ingredient_name.lower()).ingredient_id
                self.ingredients.delete_ingredient(ingredient_id)

    # TODO: same as in ut_csv_reader, can be combined later
    def __create_csv_file(self):
        with open(self.ut_file_full_name, 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            for csv_ut_data in self.recipe_ingredient_csv_data_array:
                csv_writer.writerow([csv_ut_data.ingredient_name,
                                     str(csv_ut_data.quantity),
                                     csv_ut_data.ingredient_measure_unit])

    # TODO: same as in ut_logic, can be combined later
    def __add_all_recipes(self):
        for i in range(len(self.recipes_data)):
            self.recipes.add_recipe(self.recipes_data[i].name, self.recipes_data[i].text)
            rec = self.recipes.get_recipe_by_name(self.recipes_data[i].name)
            self.recipes_data[i].recipe_id = rec.recipe_id

    # TODO: same as in ut_logic, can be combined later
    def __add_all_ingredients(self):
        for i in range(len(self.ingredients_data)):
            self.ingredients.add_ingredient(self.ingredients_data[i].name, self.ingredients_data[i].meas_unit)
            ingr = self.ingredients.get_ingredient_by_name(self.ingredients_data[i].name)
            self.ingredients_data[i].ingredient_id = ingr.ingredient_id

    # TODO: same as in ut_logic, can be combined later
    def __add_all_recipes_ingredients(self):
        for recipe_name in self.recipes_ingredients_quantity.keys():
            for ingredient_name in self.recipes_ingredients_quantity.get(recipe_name).keys():
                recipe_id = self.recipes.get_recipe_by_name(recipe_name).recipe_id
                ingredient_id = self.ingredients.get_ingredient_by_name(ingredient_name).ingredient_id
                self.recipes_ingredients.add_recipe_ingredient(recipe_id, ingredient_id,
                                                               self.recipes_ingredients_quantity
                                                               [recipe_name][ingredient_name])

    def check_print_options(self):
        self.check_not_throws(self.cmd_options_parser.print_options)

    def check_list_recipes(self):
        self.check_not_throws(self.cmd_options_parser.handle_option, '-lr')

    def check_list_ingredients(self):
        self.check_not_throws(self.cmd_options_parser.handle_option, '-li')

    def check_add_recipe_via_csv(self):
        self.check_false(self.recipes.recipe_exists(self.ut_file_name_without_extension))
        self.check_not_throws(self.cmd_options_parser.handle_option, '-af ' +
                              self.ut_file_name_without_extension + ' ' +
                              self.path)
        self.check_true(self.recipes.recipe_exists(self.ut_file_name_without_extension))

    def check_delete_recipe(self):
        self.check_true(self.recipes.recipe_exists(self.ut_file_name_without_extension))
        recipe_data = self.recipes.get_recipe_by_name(self.ut_file_name_without_extension)
        self.check_not_throws(self.cmd_options_parser.handle_option, '-dr' + ' ' + str(recipe_data.recipe_id))
        self.check_throws(self.recipes.get_recipe_by_id, recipe_data.recipe_id)

    def check_clean_ingredients(self):
        self.check_not_throws(self.cmd_options_parser.handle_option, '-ci')

    def check_create_shopping_list(self):
        self.check_not_throws(self.cmd_options_parser.handle_option,
                              '-c' + ' ' + str(self.recipes_data[0].recipe_id) + ' ' +
                              str(self.recipes_data[1].recipe_id))

    def check(self):
        self.check_print_options()
        self.check_list_recipes()
        self.check_list_ingredients()
        self.check_add_recipe_via_csv()
        self.check_delete_recipe()
        self.check_clean_ingredients()
        self.check_create_shopping_list()
