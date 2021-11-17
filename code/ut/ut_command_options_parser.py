import recipes
import command_options_parser
from ut_base import Ut
from ut_logic import UtLogic
from ut_csv_reader import UtCsvReader


class UtCommandOptionsParser(Ut):
    def __init__(self, db_filename):
        self.recipes = recipes.Recipes(db_filename)

        self.ut_logic = UtLogic(db_filename)
        self.ut_csv_reader = UtCsvReader(db_filename)
        self.cmd_options_parser = command_options_parser.CommandOptionsParser(db_filename)

    def check_print_options(self):
        self.check_not_throws(self.cmd_options_parser.print_options)

    def check_list_recipes(self):
        self.check_not_throws(self.cmd_options_parser.handle_option, '-lr')

    def check_list_ingredients(self):
        self.check_not_throws(self.cmd_options_parser.handle_option, '-li')

    def check_add_recipe_via_csv(self):
        self.check_false(self.recipes.recipe_exists(self.ut_csv_reader.ut_file_name_without_extension))
        self.check_not_throws(self.cmd_options_parser.handle_option, '-af ' +
                              self.ut_csv_reader.ut_file_name_without_extension + ' ' +
                              self.ut_csv_reader.path)
        self.check_true(self.recipes.recipe_exists(self.ut_csv_reader.ut_file_name_without_extension))

    def check_delete_recipe(self):
        self.check_true(self.recipes.recipe_exists(self.ut_csv_reader.ut_file_name_without_extension))
        recipe_data = self.recipes.get_recipe_by_name(self.ut_csv_reader.ut_file_name_without_extension)
        self.check_not_throws(self.cmd_options_parser.handle_option, '-dr' + ' ' + str(recipe_data.recipe_id))
        self.check_throws(self.recipes.get_recipe_by_id, recipe_data.recipe_id)

    def check_clean_ingredients(self):
        self.check_not_throws(self.cmd_options_parser.handle_option, '-ci')

    def check_create_shopping_list(self):
        self.check_not_throws(self.cmd_options_parser.handle_option,
                              '-c' + ' ' + str(self.ut_logic.recipes_data[0].recipe_id) + ' ' +
                              str(self.ut_logic.recipes_data[1].recipe_id))

    def check(self):
        self.check_print_options()
        self.check_list_recipes()
        self.check_list_ingredients()
        self.check_add_recipe_via_csv()
        self.check_delete_recipe()
        self.check_clean_ingredients()
        self.check_create_shopping_list()
