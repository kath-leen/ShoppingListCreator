import ingredients
from ut_base import Ut
import database


class UtIngredients(Ut):
    def __init__(self, db_filename):
        self.ingredients = ingredients.Ingredients(db_filename)
        self.ingr_name = 'potato'
        self.ingr_measure_unit = 'kg'
        self.id = 0

    def add_ingr(self):
        self.ingredients.add_ingredient(self.ingr_name, self.ingr_measure_unit)
        ingr = self.ingredients.get_ingredient_by_name(self.ingr_name)
        self.id = ingr.ingredient_id

    def delete_ingr(self):
        self.ingredients.delete_ingredient(self.id)

    def check_add_ingredient(self):
        self.add_ingr()
        ingr = self.ingredients.get_ingredient_by_id(self.id)
        self.check_equal(self.ingr_name, ingr.name)
        self.check_equal(self.ingr_measure_unit, ingr.meas_unit)

    def check_set_measurement_unit(self):
        new_measure_unit = 'g'
        self.ingredients.set_measurement_unit(self.id, new_measure_unit)
        ingr = self.ingredients.get_ingredient_by_id(self.id)
        self.check_equal(new_measure_unit, ingr.meas_unit)
        self.ingr_measure_unit = new_measure_unit

    def check_set_name(self):
        new_name = 'tomato'
        self.ingredients.set_name(self.id, new_name)
        ingr = self.ingredients.get_ingredient_by_id(self.id)
        self.check_equal(new_name, ingr.name)
        self.ingr_name = new_name

    def check_delete_ingredient(self):
        self.check_not_throws(self.ingredients.get_ingredient_by_id, self.id)
        self.delete_ingr()
        self.check_throws(self.ingredients.get_ingredient_by_id, self.id)

    def check(self):
        self.add_ingr()
        self.check_add_ingredient()
        self.check_set_measurement_unit()
        self.check_set_name()
        self.check_delete_ingredient()
