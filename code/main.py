import ingredients
import recipes
import recipes_ingredients
import database
import logic


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

    desired_recipes = logic.chooseRecipes(recipesDb)
    print(desired_recipes)
    logic.printAllSummarizedIngredients(logic.summarizeAllIngredients(desired_recipes, recIngDb), ingredientsDb)

if __name__ == '__main__':
    db_filename = '../databases/shoppingListDb'
    database.delete_table(db_filename, 'ingredients')
    database.delete_table(db_filename, 'recipes')
    database.delete_table(db_filename, 'recipes_ingredients')
    test(db_filename)