import ingredients
import recipes
import recipes_ingredients


def print_all_recipes(recipes_database):
    recipe_ids = recipes_database.get_all_ids()
    print('Here are all the available recipes')
    for recipe_id in recipe_ids:
        recipe_name = recipes_database.get_recipe_by_id(recipe_id).name
        print('{:<4s} {:<5s} {:<6s} {:<25s}'.format('id: ',
                                                    str(recipe_id),
                                                    'name: ',
                                                    recipe_name))


def print_all_ingredients(ingredients_database):
    ingredient_ids = ingredients_database.get_all_ids()
    print('Here are all the available ingredients')
    for ingredient_id in ingredient_ids:
        ingredient = ingredients_database.get_ingredient_by_id(ingredient_id)
        print('{:<4s} {:<5s} {:<6s} {:<25s} {:<20s} {:<20s}'.format('id: ',
                                                                    str(ingredient.ingredient_id),
                                                                    'name: ',
                                                                    ingredient.name,
                                                                    'measurement unit: ',
                                                                    ingredient.meas_unit))


def delete_all_unused_ingredients(ingredients_database, recipes_ingredients_database):
    ingredient_ids = ingredients_database.get_all_ids()
    for ingredient_id in ingredient_ids:
        if not recipes_ingredients_database.is_ingredient_used_anywhere(ingredient_id):
            ingredient = ingredients_database.get_ingredient_by_id(ingredient_id)
            print('Ingredient ' + ingredient.name + ' with ID ' + str(ingredient_id) +
                  ' will be deleted because it is not used in any recipe')
            ingredients_database.delete_ingredient(ingredient_id)


def add_recipe(db_filename):
    ingredients_db = ingredients.Ingredients(db_filename)
    recipes_db = recipes.Recipes(db_filename)
    recipes_ingredients_db = recipes_ingredients.RecipesIngredients(db_filename)

    recipe_name = input('Enter recipe name: ')
    if recipes_db.recipe_exists(recipe_name):
        print('There is already such recipe!')
        return
    recipe_text = input('Enter recipe description: ')

    recipes_db.add_recipe(recipe_name, recipe_text)
    recipe = recipes_db.get_recipe_by_name(recipe_name)

    ingredient_name = 'non empty string'
    while ingredient_name != '':
        ingredient_name = input('Enter ingredient name (to stop entering ingredients, just push "Enter"): ')
        if ingredient_name == '':
            break
        elif ingredients_db.ingredient_exists(ingredient_name):
            ingredient = ingredients_db.get_ingredient_by_name(ingredient_name)
            print('Found ingredient in the database: measurement unit is ' + ingredient.meas_unit)
        else:
            print('No such ingredient was found in the database, adding a new one')
            ingredient_meas_unit = input('Enter measurement unit: ')
            ingredients_db.add_ingredient(ingredient_name, ingredient_meas_unit)
            ingredient = ingredients_db.get_ingredient_by_name(ingredient_name)
        quantity = input('Enter amount in measurement units: ')
        recipes_ingredients_db.add_recipe_ingredient(recipe.recipe_id, ingredient.ingredient_id, quantity)


def delete_recipe(db_filename):
    recipes_db = recipes.Recipes(db_filename)
    ingredients_db = ingredients.Ingredients(db_filename)
    recipes_ingredients_db = recipes_ingredients.RecipesIngredients(db_filename)

    print_all_recipes(recipes_db)
    recipe_id = input('Enter recipe ID that you wish to delete ')
    recipes_db.delete_recipe(recipe_id)
    recipes_ingredients_db.delete_recipe(recipe_id)
    delete_all_unused_ingredients(ingredients_db, recipes_ingredients_db)


def choose_recipes(recipes_database):
    print_all_recipes(recipes_database)
    desired_recipes_by_id_str = input('\nPlease choose what recipes do you like to add '
                                      '(print IDs, divide by comma, do not use space) ')
    desired_recipes_by_id = desired_recipes_by_id_str.split(',')
    return desired_recipes_by_id


def summarize_all_ingredients(desired_recipes_by_id, recipes_ingredients_database):
    ingredients_summary_data = {}
    for recipe_id in desired_recipes_by_id:
        recipe_ingredients_data = recipes_ingredients_database.get_recipe_ingredients(recipe_id)
        for recipe_ingredient_data in recipe_ingredients_data:
            ingredients_summary_data[recipe_ingredient_data.ingredient_id] = \
                ingredients_summary_data.get(recipe_ingredient_data.ingredient_id, 0) + recipe_ingredient_data.quantity
    return ingredients_summary_data


def print_all_summarized_ingredients(ingredients_summary_data, ingredients_database):
    print('All ingredients you need:')
    for ingredient_id in list(ingredients_summary_data):
        ingredient = ingredients_database.get_ingredient_by_id(ingredient_id)

        print('{:<12s} {:<25s} {:<10s} {:<5s} {:<10s}'.format('ingredient:',
                                                              ingredient.name,
                                                              'quantity:',
                                                              str(ingredients_summary_data[ingredient_id]),
                                                              ingredient.meas_unit))
