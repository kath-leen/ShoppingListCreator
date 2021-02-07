from dataclasses import dataclass
import database


@dataclass
class Ingredient:
    ingredient_id: int
    name: str
    meas_unit: str


class Ingredients:
    def __init__(self, db_filename):
        self.database = database.DatabaseWrapper(db_filename)
        self.database.execute('CREATE TABLE IF NOT EXISTS ingredients ('
                              'id INTEGER PRIMARY KEY, '
                              'name TEXT, '
                              'meas_unit TEXT)')

    def get_database_wrapper(self):
        return self.database

    def add_ingredient(self, name, measurement_unit):
        if not name or not measurement_unit:
            print('Ingredients::add_ingredient: impossible to add an ingredient with the empty parameter!')
            return

        return self.database.execute_and_get_inserted_id(
            'INSERT INTO ingredients (name, meas_unit) VALUES (?, ?)',
            (name, measurement_unit)
        )

    def set_measurement_unit(self, ingredient_id, measurement_unit):
        self.database.execute('UPDATE ingredients SET measurement_unit = ? WHERE id = ?',
                              (measurement_unit, ingredient_id))

    def set_name(self, ingredient_id, name):
        self.database.execute('UPDATE ingredients SET name = ? WHERE id = ?', (name, ingredient_id))

    def get_ingredient_by_id(self, ingredient_id):
        res = self.database.execute_and_fetch_one(
            'SELECT id, name, meas_unit FROM ingredients WHERE id = ?',
            (ingredient_id,)
        )
        return Ingredient(res[0], res[1], res[2])

    def get_ingredient_by_name(self, name):
        res = self.database.execute_and_fetch_one(
            'SELECT id, name, meas_unit FROM ingredients WHERE name = ?',
            (name,)
        )
        return Ingredient(res[0], res[1], res[2])

    def delete_ingredient(self, ingredient_id):
        self.database.execute('DELETE FROM ingredients WHERE id = ?', (ingredient_id,))