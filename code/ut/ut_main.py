from ut_ingredients import UtIngredients
from ut_recipes import UtRecipes
from ut_recipes_ingredients import UtRecipesIngredients
from ut_logic import UtLogic
from ut_csv_reader import UtCsvReader
from ut_command_options_parser import UtCommandOptionsParser
import database


def test_ingredients(db_filename):
    ut_ingr = UtIngredients(db_filename)
    ut_ingr.check()


def test_recipes(db_filename):
    ut_rec = UtRecipes(db_filename)
    ut_rec.check()


def test_recipes_ingredients(db_filename):
    ut_rec_ingr = UtRecipesIngredients(db_filename)
    ut_rec_ingr.check()


def test_logic(db_filename):
    ut_logic = UtLogic(db_filename)
    ut_logic.check()


def test_csv_reader(db_filename):
    ut_csv_reader = UtCsvReader(db_filename)
    ut_csv_reader.check()


def test_command_options_parser(db_filename):
    ut_cmd_options_parser = UtCommandOptionsParser(db_filename)
    ut_cmd_options_parser.check()


if __name__ == '__main__':
    db_filename = '../../databases/shoppingListDbTest'
    database.delete_table(db_filename, 'ingredients')
    database.delete_table(db_filename, 'recipes')
    database.delete_table(db_filename, 'recipes_ingredients')
    test_ingredients(db_filename)
    test_recipes(db_filename)
    test_recipes_ingredients(db_filename)
    test_logic(db_filename)
    test_csv_reader(db_filename)
    test_command_options_parser(db_filename)
