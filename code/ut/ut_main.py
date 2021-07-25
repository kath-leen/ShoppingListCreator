from ut_ingredients import UtIngredients
from ut_recipes import UtRecipes
from ut_recipes_ingredients import UtRecipesIngredients
import database


def test_ingredients(db_filename):
    utIngr = UtIngredients(db_filename)
    utIngr.check()


def test_recipes(db_filename):
    utRec = UtRecipes(db_filename)
    utRec.check()


def test_recipes_ingredients(db_filename):
    utRecIngr = UtRecipesIngredients(db_filename)
    utRecIngr.check()


if __name__ == '__main__':
    db_filename = '../../databases/shoppingListDb'
    database.delete_table(db_filename, 'ingredients')
    database.delete_table(db_filename, 'recipes')
    database.delete_table(db_filename, 'recipes_ingredients')
    test_ingredients(db_filename)
    test_recipes(db_filename)
    test_recipes_ingredients(db_filename)