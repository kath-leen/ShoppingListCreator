from dataclasses import dataclass
import csv
import ingredients
import recipes
import recipes_ingredients

@dataclass
class RecipeIngredientCsvData:
    ingredient_name: int
    quantity: float
    ingredient_measure_unit: int
    to_add_new_ingredient: bool


class CsvReader:
    def __init__(self, db_filename, file_name_without_extension, path='../csv'):
        self.ingredients_db = ingredients.Ingredients(db_filename)
        self.recipes_db = recipes.Recipes(db_filename)
        self.recipes_ingredients_db = recipes_ingredients.RecipesIngredients(db_filename)
        self.file_name_without_extension = file_name_without_extension
        self.path = path
        self.recipe_name = ''
        self.recipe_list = []

    def __get_recipe_name(self):
        local_recipe_name = self.file_name_without_extension
        input_value = input('Is ' + self.file_name_without_extension + ' the desired recipe name or do you want to '
                                                                  'enter a new one? Enter y if yes or enter the right '
                                                                  'name if you wish to enter a new name: ')
        if input_value != 'y':
            local_recipe_name = input_value
            print('New recipe name is: ' + local_recipe_name)

        if self.recipes_db.recipe_exists(local_recipe_name):
            recipe_id = self.recipes_db.get_recipe_by_name(local_recipe_name).recipe_id
            if input('Sorry, the recipe with this name already exists! Do you want to delete the old recipe? (y/n) ') \
                    == 'y':
                self.recipes_ingredients_db.delete_recipe(recipe_id)
                self.recipes_db.delete_recipe(recipe_id)
            else:
                raise Exception('Recipe already exists!')
        self.recipe_name = local_recipe_name

    def __analyze_row_and_form_the_list(self, row):
        if len(row) != 3:
            raise Exception('Incorrect row format!')

        ingr_name = row[0].lower()
        ingr_quantity = float(row[1])
        ingr_meas_unit = row[2].lower()

        print('DBG: Ingredient name: ' + ingr_name + ', ingredient quantity: ' + row[1] + ', measure unit: ' + ingr_meas_unit)

        if self.ingredients_db.ingredient_exists(ingr_name):
            ingredient = self.ingredients_db.get_ingredient_by_name(ingr_name)
            if ingredient.meas_unit == ingr_meas_unit:
                self.recipe_list.append(RecipeIngredientCsvData(ingredient.name, ingr_quantity, ingredient.meas_unit,
                                                                False))
            else:
                choice = input('Ingredient measure unit in CSV is ' + ingr_meas_unit +
                            ' while in database it is ' + ingredient.meas_unit +
                            '. Please enter 1 if it is the same and ' +  ingredient.meas_unit +
                            ' can be used or 2 to convert ' + ingr_meas_unit + ' to ' + ingredient.meas_unit + ': ')
                if choice == '1':
                    self.recipe_list.append(
                        RecipeIngredientCsvData(ingredient.name, ingr_quantity, ingredient.meas_unit, False))
                else:
                    new_quantity = input('Please enter new quantity in ' + ingredient.meas_unit +
                                         '(the old one in ' + ingr_meas_unit + ' was ' + row[1] + '): ')
                    ingr_quantity = float(new_quantity)
                    self.recipe_list.append\
                        (RecipeIngredientCsvData(ingredient.name, ingr_quantity, ingredient.meas_unit, False))
        else:
            self.recipe_list.append(RecipeIngredientCsvData(ingr_name, ingr_quantity, ingr_meas_unit, True))

    def __add_the_recipe_to_databases(self):
        self.recipes_db.add_recipe(self.recipe_name)
        recipe_data = self.recipes_db.get_recipe_by_name(self.recipe_name)
        for ingr_data in self.recipe_list:
            print('DBG: From the list: Ingredient name: ' + ingr_data.ingredient_name + ', ingredient quantity: ' +
                  str(ingr_data.quantity) + ', measure unit: ' + ingr_data.ingredient_measure_unit+ ', to add: ' +
                  str(ingr_data.to_add_new_ingredient))
            if ingr_data.to_add_new_ingredient:
                self.ingredients_db.add_ingredient(ingr_data.ingredient_name, ingr_data.ingredient_measure_unit)
            ingredient_data = self.ingredients_db.get_ingredient_by_name(ingr_data.ingredient_name)
            self.recipes_ingredients_db.add_recipe_ingredient(recipe_data.recipe_id, ingredient_data.ingredient_id,
                                                              ingr_data.quantity)

    def read_csv_and_add_to_database(self):
        try:
            self.__get_recipe_name()
        except Exception:
            return False

        with open(self.path + '/' + self.file_name_without_extension + '.csv', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            try:
                for row in csv_reader:
                    self.__analyze_row_and_form_the_list(row)
            except Exception:
                return False
            self.__add_the_recipe_to_databases()

        return True
