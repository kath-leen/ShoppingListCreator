from ut_ingredients import UtIngredients
from ut_recipes import UtRecipes
import database


def test_ingredients(db_filename):
    utIngr = UtIngredients(db_filename)
    utIngr.check()


def test_recipes(db_filename):
    utRec = UtRecipes(db_filename)
    utRec.check()


if __name__ == '__main__':
    db_filename = '../../databases/shoppingListDb'
    database.delete_table(db_filename, 'ingredients')
    database.delete_table(db_filename, 'recipes')
    test_ingredients(db_filename)
    test_recipes(db_filename)