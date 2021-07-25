from ut_ingredients import UtIngredients
import database


def test_ingredients(db_filename):
    utIngr = UtIngredients(db_filename)
    utIngr.check()


if __name__ == '__main__':
    db_filename = '../../databases/shoppingListDb'
    database.delete_table(db_filename, 'ingredients')
    test_ingredients(db_filename)