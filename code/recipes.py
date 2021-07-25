from dataclasses import dataclass
import database


@dataclass
class Recipe:
    recipe_id: int
    name: str
    text: str  # a recipe itself or a link to it


class Recipes:
    def __init__(self, db_filename):
        self.database = database.DatabaseWrapper(db_filename)
        self.database.execute('CREATE TABLE IF NOT EXISTS recipes ('
                              'id INTEGER PRIMARY KEY, '
                              'name TEXT, '
                              'text TEXT)')

    def get_database_wrapper(self):
        return self.database

    def add_recipe(self, name, text=''):
        if not name:
            print('Recipes::add_recipe: impossible to add a recipe with the empty name!')
            return

        return self.database.execute_and_get_inserted_id(
            'INSERT INTO recipes (name, text) VALUES (?, ?)', (name, text)
        )

    def set_name(self, recipe_id, name):
        self.database.execute('UPDATE recipes SET name = ? WHERE id = ?', (name, recipe_id))

    def set_text(self, recipe_id, text):
        self.database.execute('UPDATE recipes SET text = ? WHERE id = ?', (text, recipe_id))

    def get_recipe_by_id(self, recipe_id):
        res = self.database.execute_and_fetch_one(
            'SELECT id, name, text FROM recipe WHERE id = ?',
            (recipe_id,)
        )
        return Recipe(res[0], res[1], res[2])

    def get_recipe_by_name(self, name):
        res = self.database.execute_and_fetch_one(
            'SELECT id, name, text FROM recipes WHERE name = ?',
            (name,)
        )
        return Recipe(res[0], res[1], res[2])

    def delete_recipe(self, recipe_id):
        self.database.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))