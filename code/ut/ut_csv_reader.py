from dataclasses import dataclass
from ut_base import Ut
import csv_reader
import recipes
import ingredients
import recipes_ingredients
import csv
import os

@dataclass
class RecipeIngredientCsvUtData:
    ingredient_name: int
    quantity: float
    ingredient_measure_unit: int

class UtCsvReader(Ut):
    def __init__(self, db_filename):
        self.recipe_ingredient_data_array = [RecipeIngredientCsvUtData('Potato', 0.5, 'grams'),
                                             RecipeIngredientCsvUtData('carrot', 0.3, 'kilograms')]
        self.ut_file_name_without_extension = 'recipe_ut_csv'
        self.path = '../../csv'
        self.ut_file_full_name = self.path + self.ut_file_name_without_extension + '.csv'

        if os.path.exists(self.ut_file_full_name):
            os.remove(self.ut_file_full_name)

        self.__create_csv_file()
        self.csv_reader = csv_reader.CsvReader(db_filename, self.ut_file_name_without_extension, self.path)

        self.recipes = recipes.Recipes(db_filename)
        self.ingredients = ingredients.Ingredients(db_filename)
        self.recipes_ingredients = recipes_ingredients.RecipesIngredients(db_filename)

    def __del__(self):
        if os.path.exists(self.ut_file_full_name):
            os.remove(self.ut_file_full_name)

    def __create_csv_file(self):
        with open(self.ut_file_full_name, 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            for csv_ut_data in self.recipe_ingredient_data_array:
                csv_writer.writerow([csv_ut_data.ingredient_name,
                                     str(csv_ut_data.quantity),
                                     csv_ut_data.ingredient_measure_unit])

    def check_read_csv_and_add_to_database(self):
        recipe_name = self.ut_file_name_without_extension
        self.recipes_ingredients.delete_recipe(recipe_name)

        if self.recipes.recipe_exists(recipe_name):
            recipe_data = self.recipes.get_recipe_by_name(recipe_name)
            self.recipes.delete_recipe(recipe_data.recipe_id)
        self.check_false(self.recipes.recipe_exists(recipe_name))

        for csv_ut_data in self.recipe_ingredient_data_array:
            ingredient_name = csv_ut_data.ingredient_name.lower()
            if self.ingredients.ingredient_exists(ingredient_name):
                ingredient_data = self.ingredients.get_ingredient_by_name(cingredient_name)
                self.ingredients.delete_ingredient(ingredient_data.ingredient_id)
            self.check_false(self.ingredients.ingredient_exists(ingredient_name))

        self.csv_reader.read_csv_and_add_to_database()

        self.check_true(self.recipes.recipe_exists(recipe_name))
        recipe_data = self.recipes.get_recipe_by_name(recipe_name)

        for csv_ut_data in self.recipe_ingredient_data_array:
            ingredient_name = csv_ut_data.ingredient_name.lower()
            self.check_true(self.ingredients.ingredient_exists(ingredient_name))
            ingredient_data = self.ingredients.get_ingredient_by_name(ingredient_name)
            self.check_equal(ingredient_data.meas_unit, csv_ut_data.ingredient_measure_unit)
            self.check_not_throws(self.recipes_ingredients.get_recipe_ingredient,
                                  recipe_data.recipe_id,
                                  ingredient_data.ingredient_id)
            rec_ingr_data = self.recipes_ingredients.get_recipe_ingredient(recipe_data.recipe_id,
                                                                           ingredient_data.ingredient_id)
            self.check_equal(rec_ingr_data.quantity, csv_ut_data.quantity)

        self.recipes_ingredients.delete_recipe(recipe_name)
        self.recipes.delete_recipe(recipe_data.recipe_id)
        for csv_ut_data in self.recipe_ingredient_data_array:
            ingredient_name = csv_ut_data.ingredient_name.lower()
            ingredient_data = self.ingredients.get_ingredient_by_name(ingredient_name)
            self.ingredients.delete_ingredient(ingredient_data.ingredient_id)

    def check(self):
        # print 'y' when the program asks you to do so
        self.check_read_csv_and_add_to_database()
