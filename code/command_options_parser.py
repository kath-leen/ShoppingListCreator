import ingredients
import recipes
import recipes_ingredients
import logic
import csv_reader


class CommandOptionsParser:
    def __init__(self, db_filename):
        self.db_filename = db_filename
        self.ingredients_db = ingredients.Ingredients(db_filename)
        self.recipes_db = recipes.Recipes(db_filename)
        self.recipes_ingredients_db = recipes_ingredients.RecipesIngredients(db_filename)
        self.option_handler_functions = {'-h': self.print_options,
                                         '-lr': self.__list_recipes,
                                         '-li': self.__list_ingredients,
                                         '-dr': self.__delete_recipe,
                                         '-ci': self.__clean_ingredients,
                                         '-am': self.__add_recipe_manually,
                                         '-af': self.__add_recipe_via_csv,
                                         '-c': self.__create_shopping_list,
                                         '-q': self.__quit}

    @staticmethod
    def print_options():
        print('-h: help (list all options)')
        print('-lr: list all recipes')
        print('-li: list all ingredients')
        print('-dr <recipe_id>: delete recipe')
        print('-ci: clean ingredients (delete unused ones)')
        print('-am: add recipe manually')
        print('-af <file_name_without_extention> <path>: add recipe via csv file (default path is ../csv)')
        print('-c <first_recipe_id> ... <last_recipe_id>: create shopping list based on the chosen recipes')
        print('-q quit')

    def __list_recipes(self):
        logic.print_all_recipes(self.recipes_db)

    def __list_ingredients(self):
        logic.print_all_ingredients(self.ingredients_db)

    def __delete_recipe(self, recipe_id):
        logic.delete_recipe(self.recipes_db, self.recipes_ingredients_db, recipe_id)

    def __clean_ingredients(self):
        logic.delete_all_unused_ingredients(self.ingredients_db, self.recipes_ingredients_db)

    def __add_recipe_manually(self):
        logic.add_recipe(db_filename)

    def __add_recipe_via_csv(self, file_name, file_path = '../csv'):
        new_csv_reader = csv_reader.CsvReader(self.db_filename, file_name, file_path)
        new_csv_reader.read_csv_and_add_to_database()

    def __create_shopping_list(self, *recipe_ids):
        logic.print_all_summarized_ingredients(logic.summarize_all_ingredients([int(recipe_id)
                                                                                for recipe_id in recipe_ids],
                                                                               self.recipes_ingredients_db),
                                               self.ingredients_db)
    @staticmethod
    def __quit():
        quit()

    def handle_option(self, option):
        split_option = option.split(' ')
        if split_option[0] not in self.option_handler_functions.keys():
            print('Unknown option! Use -h to list all possible options')
            return

        if split_option[0] == '-dr':
            if len(split_option) < 2:
                print('Unknown parameter! Use recipe ID to specify the deleted recipe. '
                      'Use -h to list all possible options with syntax')
            else:
                self.option_handler_functions[split_option[0]](split_option[1])
        elif split_option[0] == '-af':
            if len(split_option) < 2:
                print('Unknown parameter! Specify csv file name and possibly path. '
                      'Use -h to list all possible options with syntax')
            elif len(split_option) == 2:
                self.option_handler_functions[split_option[0]](split_option[1])
            else:
                self.option_handler_functions[split_option[0]](split_option[1], split_option[2])
        elif split_option[0] == '-c':
            if len(split_option) < 2:
                print('Please mention at least one recipe ID. '
                      'Use -h to list all possible options with syntax')
            else:
                arguments = split_option[1:]
                self.option_handler_functions[split_option[0]](*arguments)
        else:
            self.option_handler_functions[split_option[0]]()
