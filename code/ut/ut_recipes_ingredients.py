import recipes_ingredients
import recipes
import ingredients
from ut_base import Ut

class UtRecipesIngredients(Ut):
    def __init__(self, db_filename):
        self.recipes = recipes.Recipes(db_filename)
        self.ingredients = ingredients.Ingredients(db_filename)
        self.recipies_ingredients = recipes_ingredients.RecipesIngredients(db_filename)
        self.recipe_name = 'oat milk porridge'
        self.recipe_text = 'add milk, heat it until boiling, add oat and boil on small heat for 3-5 minutes'
        self.recipe_id = 0
        self.ingredient_names = ['oat', 'milk']
        self.meas_units = ['g', 'l']
        self.ingredients_ids = [0, 0]
        self.ingredients_quantities = [50, 1]
        self.check_equal(len(self.ingredient_names), len(self.meas_units))
        self.check_equal(len(self.ingredient_names), len(self.ingredients_ids))
        self.check_equal(len(self.ingredient_names), len(self.ingredients_quantities))

    def add_recipe(self):
        self.recipes.add_recipe(self.recipe_name, self.recipe_text)
        rec = self.recipes.get_recipe_by_name(self.recipe_name)
        self.recipe_id = rec.recipe_id

    def add_all_ingredients(self):
        for i in range(len(self.ingredient_names)):
            self.ingredients.add_ingredient(self.ingredient_names[i], self.meas_units[i])
            ingr = self.ingredients.get_ingredient_by_name(self.ingredient_names[i])
            self.ingredients_ids[i] = ingr.ingredient_id

    def add_rec_ingr(self, index):
        self.check_true(index < len(self.ingredient_names))
        self.recipies_ingredients.add_recipe_ingredient(self.recipe_id, self.ingredients_ids[index],
                                                        self.ingredients_quantities[index])

    def delete_ingr_from_rec(self, index):
        self.check_true(index < len(self.ingredient_names))
        self.recipies_ingredients.delete_ingredient_from_recipe(self.recipe_id, self.ingredients_ids[index])

    def delete_rec(self):
        self.recipies_ingredients.delete_recipe(self.recipe_id)

    def check_add_rec_ingr(self):
        for i in range(len(self.ingredients_ids)):
            self.add_rec_ingr(i)
            rec_ingr = self.recipies_ingredients.get_recipe_ingredient(self.recipe_id, self.ingredients_ids[i])
            self.check_equal(rec_ingr.recipe_id, self.recipe_id)
            self.check_equal(rec_ingr.ingredient_id, self.ingredients_ids[i])
            self.check_equal(rec_ingr.quantity, self.ingredients_quantities[i])

    def check_get_recipe_ingredients(self):
        rec_all_ingr = self.recipies_ingredients.get_recipe_ingredients(self.recipe_id)
        for i in range(len(self.ingredients_ids)):
            self.check_equal(rec_all_ingr[i].recipe_id, self.recipe_id)
            self.check_equal(rec_all_ingr[i].ingredient_id, self.ingredients_ids[i])
            self.check_equal(rec_all_ingr[i].quantity, self.ingredients_quantities[i])


    def check_set_quantity(self):
        new_quantities = [100, 2]
        self.check_equal(len(new_quantities), len(self.ingredients_quantities))
        for i in range(len(self.ingredients_ids)):
            self.recipies_ingredients.set_quantity(self.recipe_id, self.ingredients_ids[i], new_quantities[i])
            rec_ingr = self.recipies_ingredients.get_recipe_ingredient(self.recipe_id, self.ingredients_ids[i])
            self.check_equal(rec_ingr.quantity, new_quantities[i])
            self.ingredients_quantities[i] = new_quantities[i]

    def check_delete_ingr_from_rec(self):
        for i in range(len(self.ingredients_ids)):
            self.check_not_throws(self.recipies_ingredients.get_recipe_ingredient, self.recipe_id,
                                  self.ingredients_ids[i])
            self.delete_ingr_from_rec(i)
            self.check_throws(self.recipies_ingredients.get_recipe_ingredient, self.recipe_id, self.ingredients_ids[i])

    def check_delete_rec(self):
        self.check_not_throws(self.recipies_ingredients.get_recipe_ingredients, self.recipe_id)
        self.delete_rec()
        self.check_throws(self.recipies_ingredients.get_recipe_ingredient, self.recipe_id)

    def check(self):
        self.add_recipe()
        self.add_all_ingredients()
        self.check_add_rec_ingr()
        self.check_get_recipe_ingredients()
        self.check_set_quantity()
        self.check_delete_ingr_from_rec()
        self.check_delete_rec()