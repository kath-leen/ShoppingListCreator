import ingredients
import recipes
import recipes_ingredients


class DatabaseLogic:
    def __init__(self, db_filename):
        self.db_filename = db_filename
        self.ingredients_db = ingredients.Ingredients(db_filename)
        self.recipes_db = recipes.Recipes(db_filename)
        self.recipes_ingredients_db = recipes_ingredients.RecipesIngredients(db_filename)

    def __print_all_summarized_ingredients(self, ingredients_summary_data):
        print('All ingredients you need:')
        for ingredient_id in list(ingredients_summary_data):
            ingredient = self.ingredients_db.get_ingredient_by_id(ingredient_id)

            print('{:<12s} {:<25s} {:<10s} {:<5s} {:<10s}'.format('ingredient:',
                                                                  ingredient.name,
                                                                  'quantity:',
                                                                  str(ingredients_summary_data[ingredient_id]),
                                                                  ingredient.meas_unit))

    def print_all_recipes(self):
        recipe_ids = self.recipes_db.get_all_ids()
        print('Here are all the available recipes')
        for recipe_id in recipe_ids:
            recipe_name = self.recipes_db.get_recipe_by_id(recipe_id).name
            print('{:<4s} {:<5s} {:<6s} {:<25s}'.format('id: ',
                                                        str(recipe_id),
                                                        'name: ',
                                                        recipe_name))

    def print_all_ingredients(self):
        ingredient_ids = self.ingredients_db.get_all_ids()
        print('Here are all the available ingredients')
        for ingredient_id in ingredient_ids:
            ingredient = self.ingredients_db.get_ingredient_by_id(ingredient_id)
            print('{:<4s} {:<5s} {:<6s} {:<25s} {:<20s} {:<20s}'.format('id: ',
                                                                        str(ingredient.ingredient_id),
                                                                        'name: ',
                                                                        ingredient.name,
                                                                        'measurement unit: ',
                                                                        ingredient.meas_unit))

    def delete_all_unused_ingredients(self):
        ingredient_ids = self.ingredients_db.get_all_ids()
        for ingredient_id in ingredient_ids:
            if not self.recipes_ingredients_db.is_ingredient_used_anywhere(ingredient_id):
                ingredient = self.ingredients_db.get_ingredient_by_id(ingredient_id)
                print('Ingredient ' + ingredient.name + ' with ID ' + str(ingredient_id) +
                      ' will be deleted because it is not used in any recipe')
                self.ingredients_db.delete_ingredient(ingredient_id)

    def add_recipe_manually(self):
        recipe_name = input('Enter recipe name: ')
        if self.recipes_db.recipe_exists(recipe_name):
            print('There is already such recipe!')
            return
        recipe_text = input('Enter recipe description: ')

        self.recipes_db.add_recipe(recipe_name, recipe_text)
        recipe = self.recipes_db.get_recipe_by_name(recipe_name)

        ingredient_name = 'non empty string'
        while ingredient_name != '':
            ingredient_name = input('Enter ingredient name (to stop entering ingredients, just push "Enter"): ')
            if ingredient_name == '':
                break
            elif self.ingredients_db.ingredient_exists(ingredient_name):
                ingredient = self.ingredients_db.get_ingredient_by_name(ingredient_name)
                print('Found ingredient in the database: measurement unit is ' + ingredient.meas_unit)
            else:
                print('No such ingredient was found in the database, adding a new one')
                ingredient_meas_unit = input('Enter measurement unit: ')
                self.ingredients_db.add_ingredient(ingredient_name, ingredient_meas_unit)
                ingredient = self.ingredients_db.get_ingredient_by_name(ingredient_name)
            quantity = input('Enter amount in measurement units: ')
            self.recipes_ingredients_db.add_recipe_ingredient(recipe.recipe_id, ingredient.ingredient_id, quantity)

    def delete_recipe_manually(self):
        self.print_all_recipes()
        recipe_id = input('Enter recipe ID that you wish to delete ')
        self.delete_recipe(recipe_id)

    def delete_recipe(self, recipe_id):
        self.recipes_db.delete_recipe(recipe_id)
        self.recipes_ingredients_db.delete_recipe(recipe_id)

    def choose_recipes(self):
        self.print_all_recipes()
        desired_recipes_by_id_str = input('\nPlease choose what recipes do you like to add '
                                          '(print IDs, divide by comma, do not use space) ')
        desired_recipes_by_id = desired_recipes_by_id_str.split(',')
        return desired_recipes_by_id

    def summarize_all_ingredients(self, desired_recipes_by_id):
        ingredients_summary_data = {}
        for recipe_id in desired_recipes_by_id:
            recipe_ingredients_data = self.recipes_ingredients_db.get_recipe_ingredients(recipe_id)
            for recipe_ingredient_data in recipe_ingredients_data:
                ingredients_summary_data[recipe_ingredient_data.ingredient_id] = \
                    ingredients_summary_data.get(recipe_ingredient_data.ingredient_id, 0) + \
                    recipe_ingredient_data.quantity
        return ingredients_summary_data

    def summarize_and_print_all_ingredients(self, desired_recipes_by_id):
        self.__print_all_summarized_ingredients(self.summarize_all_ingredients(desired_recipes_by_id))
