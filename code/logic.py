import ingredients
import recipes
import recipes_ingredients

def choose_recipes(recipes_database):
    recipe_ids = recipes_database.get_all_ids()
    print('Here are all the available recipes')
    for recipe_id in recipe_ids:
        recipe_name = recipes_database.get_recipe_by_id(recipe_id).name
        print('id: ' + str(recipe_id) + ', name: ' + recipe_name)
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
