from ../ import ingredients
import ut_base
import database


class UtIngredients(Ut):
    def __init__(self, db_filename):
        self.ingredients = Ingredients(db_filename)
        self.ingr_name = 'potato'
        self.ingr_measure_unit = 'kg'
        self.id = 0

    def add_ingr(self):
        ingredients.add_ingredient(ingr_name, ingr_measure_unit)
        ingr = ingredients.get_ingredient_by_name(ingr_name)
        id = ingr.ingredient_id

    def check_add_ingredient(self):
        add_ingr()
        ingr = ingredients.get_ingredient_by_id(id)
        check_equal(ingr_name, ingr.name)
        check_equal(ingr_measure_unit, ingr.meas_unit)

    def check_set_measurement_unit(self):
        new_measure_unit = 'g'
        ingredients.set_measurement_unit(id, new_measure_unit)
        ingr = ingredients.get_ingredient_by_id(id)
        check_equal(new_measure_unit, ingr.meas_unit)
        ingr_measure_unit = new_measure_unit

    def check_set_name(self):
        new_name = 'tomato'
        ingredients.set_name(id, new_name)
        ingr = ingredients.get_ingredient_by_id(id)
        check_equal(new_name, ingr.name)
        ingr_name = new_name

    def check_delete_ingredient(self):
        delete_ingredient(id)
        # todo

    def check(self):
        add_ingr()
        check_add_ingredient()
        check_set_measurement_unit()
        check_set_name()
        check_delete_ingredient()


if __name__ == '__main__':
    db_filename = '../databases/shoppingListDb'
    database.delete_table(db_filename, 'ingredients')

    ut_ingredients = UtIngredients(db_filename)
    ut_ingredients.check()