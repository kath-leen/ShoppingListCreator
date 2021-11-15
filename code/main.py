import ingredients
import recipes
import recipes_ingredients
import database
import logic
import command_options_parser


isTest = False


def test(db_filename):
    db_logic = logic.DatabaseLogic(db_filename)
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

    # db_logic.add_recipe()

    desired_recipes = db_logic.choose_recipes()
    print(desired_recipes)
    db_logic.summarize_and_print_all_ingredients(desired_recipes)

    db_logic.delete_recipe_manually()
    db_logic.print_all_recipes()
    db_logic.print_all_ingredients()

    print('\nNow all the unused ingredients will be removed')
    db_logic.delete_all_unused_ingredients()
    db_logic.print_all_ingredients()


def run_test():
    db_filename = '../databases/shoppingListDbTest'
    database.delete_table(db_filename, 'ingredients')
    database.delete_table(db_filename, 'recipes')
    database.delete_table(db_filename, 'recipes_ingredients')
    test(db_filename)


def run_real():
    db_filename = '../databases/shoppingListDb'
    cmd_options_parser = command_options_parser.CommandOptionsParser(db_filename)
    print('Starting the program. Possible options are:')
    cmd_options_parser.print_options()
    while True:
        option = input('\n')
        cmd_options_parser.handle_option(option)


if __name__ == '__main__':
    if isTest:
        run_test()
    else:
        run_real()
