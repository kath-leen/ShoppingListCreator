import ingredients
import recipes
import recipes_ingredients
import database
import logic

isTest = False

def test(db_filename):
    recipesDb = recipes.Recipes(db_filename)
    ingredientsDb = ingredients.Ingredients(db_filename)
    ingredientsDb.add_ingredient('carrot', 'kg')
    ingredientsDb.add_ingredient('potato', 'kg')
    ingredientsDb.add_ingredient('milk', 'l')
    ingredientsDb.add_ingredient('banana', 'pieces')
    recipesDb.add_recipe('carrot_stuff', 'just cut and bake')
    recipesDb.add_recipe('miklshake')

    rec_carrot_stuff = recipesDb.get_recipe_by_name('carrot_stuff')
    rec_milkshake = recipesDb.get_recipe_by_name('miklshake')

    ing_carrot = ingredientsDb.get_ingredient_by_name('carrot')
    ing_potato = ingredientsDb.get_ingredient_by_name('potato')
    ing_milk = ingredientsDb.get_ingredient_by_name('milk')
    ing_banana = ingredientsDb.get_ingredient_by_name('banana')

    recIngDb = recipes_ingredients.RecipesIngredients(db_filename)
    recIngDb.add_recipe_ingredient(rec_carrot_stuff.recipe_id, ing_carrot.ingredient_id, 0.3)
    recIngDb.add_recipe_ingredient(rec_carrot_stuff.recipe_id, ing_potato.ingredient_id, 0.2)
    recIngDb.add_recipe_ingredient(rec_carrot_stuff.recipe_id, ing_milk.ingredient_id, 0.5)
    recIngDb.add_recipe_ingredient(rec_milkshake.recipe_id, ing_milk.ingredient_id, 1)
    recIngDb.add_recipe_ingredient(rec_milkshake.recipe_id, ing_banana.ingredient_id, 2)

    print(recIngDb.get_recipe_ingredients(rec_carrot_stuff.recipe_id))
    print(recIngDb.get_recipe_ingredients(rec_milkshake.recipe_id))

    # logic.add_recipe(db_filename)

    desired_recipes = logic.choose_recipes(recipesDb)
    print(desired_recipes)
    logic.print_all_summarized_ingredients(logic.summarize_all_ingredients(desired_recipes, recIngDb), ingredientsDb)

    logic.delete_recipe(db_filename)
    logic.print_all_recipes(recipesDb)
    logic.print_all_ingredients(ingredientsDb)


def run_test():
    db_filename = '../databases/shoppingListDbTest'
    database.delete_table(db_filename, 'ingredients')
    database.delete_table(db_filename, 'recipes')
    database.delete_table(db_filename, 'recipes_ingredients')
    test(db_filename)


def run_real():
    db_filename = '../databases/shoppingListDb'
    recipes_db = recipes.Recipes(db_filename)
    ingredients_db = ingredients.Ingredients(db_filename)
    recipes_ingredients_db = recipes_ingredients.RecipesIngredients(db_filename)

    print('Current database content is: ')
    logic.print_all_recipes(recipes_db)
    logic.print_all_ingredients(ingredients_db)

    answer = input('\nDo you want to remove some recipe? (enter y or n) ')
    while answer == 'y':
        logic.delete_recipe(db_filename)
        answer = input('Do you want to remove another recipe? (enter y or n) ')

    answer = input('\nDo you want to add a new recipe? (enter y or n) ')
    while answer == 'y':
        logic.add_recipe(db_filename)
        answer = input('Do you want to add another recipe? (enter y or n) ')

    print('\n')
    desired_recipes = logic.choose_recipes(recipes_db)

    print('\n')
    logic.print_all_summarized_ingredients(logic.summarize_all_ingredients(desired_recipes, recipes_ingredients_db),
                                           ingredients_db)


if __name__ == '__main__':
    if isTest:
        run_test()
    else:
        run_real()
