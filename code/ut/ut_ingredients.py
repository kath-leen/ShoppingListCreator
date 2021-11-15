import ingredients
from ut_base import Ut


class UtIngredients(Ut):
    def __init__(self, db_filename):
        self.ingredients = ingredients.Ingredients(db_filename)
        self.ingr_name = 'potato'
        self.ingr_measure_unit = 'kg'
        self.id = 0
        self.non_existed_ingr_name = 'unknown ingredient'

    def __del__(self):
        if self.ingredients.ingredient_exists(self.ingr_name):
            self.ingredients.delete_ingredient(self.id)

    def __add_ingr(self):
        self.ingredients.add_ingredient(self.ingr_name, self.ingr_measure_unit)
        ingr = self.ingredients.get_ingredient_by_name(self.ingr_name)
        self.id = ingr.ingredient_id

    def __delete_ingr(self):
        self.ingredients.delete_ingredient(self.id)

    def check_add_ingredient(self):
        self.__add_ingr()
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
        self.__delete_ingr()
        self.check_throws(self.ingredients.get_ingredient_by_id, self.id)

    def check_ingredient_exists(self):
        self.check_true(self.ingredients.ingredient_exists(self.ingr_name))
        self.check_false(self.ingredients.ingredient_exists(self.non_existed_ingr_name))

    def check(self):
        self.check_add_ingredient()
        self.check_set_measurement_unit()
        self.check_set_name()
        self.check_ingredient_exists()
        self.check_delete_ingredient()
