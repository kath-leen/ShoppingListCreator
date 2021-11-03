import ingredients
import recipes
import recipes_ingredients
import database
import logic


isTest = False


def test(db_filename):
    recipes_db = recipes.Recipes(db_filename)
    ingredients_db = ingredients.Ingredients(db_filename)
    ingredients_db.add_ingredient('carrot', 'kg')
    ingredients_db.add_ingredient('potato', 'kg')
    ingredients_db.add_ingredient('milk', 'l')
    ingredients_db.add_ingredient('banana', 'pieces')
    recipes_db.add_recipe('carrot_stuff', 'just cut and bake')
    recipes_db.add_recipe('miklshake')

    rec_carrot_stuff = recipes_db.get_recipe_by_name('carrot_stuff')
    rec_milkshake = recipes_db.get_recipe_by_name('miklshake')

    ing_carrot = ingredients_db.get_ingredient_by_name('carrot')
    ing_potato = ingredients_db.get_ingredient_by_name('potato')
    ing_milk = ingredients_db.get_ingredient_by_name('milk')
    ing_banana = ingredients_db.get_ingredient_by_name('banana')

    rec_ing_db = recipes_ingredients.RecipesIngredients(db_filename)
    rec_ing_db.add_recipe_ingredient(rec_carrot_stuff.recipe_id, ing_carrot.ingredient_id, 0.3)
    rec_ing_db.add_recipe_ingredient(rec_carrot_stuff.recipe_id, ing_potato.ingredient_id, 0.2)
    rec_ing_db.add_recipe_ingredient(rec_carrot_stuff.recipe_id, ing_milk.ingredient_id, 0.5)
    rec_ing_db.add_recipe_ingredient(rec_milkshake.recipe_id, ing_milk.ingredient_id, 1)
    rec_ing_db.add_recipe_ingredient(rec_milkshake.recipe_id, ing_banana.ingredient_id, 2)

    print(rec_ing_db.get_recipe_ingredients(rec_carrot_stuff.recipe_id))
    print(rec_ing_db.get_recipe_ingredients(rec_milkshake.recipe_id))

    # logic.add_recipe(db_filename)

    desired_recipes = logic.choose_recipes(recipes_db)
    print(desired_recipes)
    logic.print_all_summarized_ingredients(logic.summarize_all_ingredients(desired_recipes, rec_ing_db), ingredients_db)

    logic.delete_recipe(db_filename)
    logic.print_all_recipes(recipes_db)
    logic.print_all_ingredients(ingredients_db)


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
