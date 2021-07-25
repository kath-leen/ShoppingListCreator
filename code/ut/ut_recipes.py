import recipes
from ut_base import Ut


class UtRecipes(Ut):
    def __init__(self, db_filename):
        self.recipes = recipes.Recipes(db_filename)
        self.recipe_name = 'boiled potato'
        self.recipe_text = 'brush potato and boil for 20-30 minutes'
        self.id = 0

    def add_recipe(self):
        self.recipes.add_recipe(self.recipe_name, self.recipe_text)
        rec = self.recipes.get_recipe_by_name(self.recipe_name)
        self.id = rec.recipe_id

    def delete_recipe(self):
        self.recipes.delete_recipe(self.id)

    def check_add_recipe(self):
        self.add_recipe()
        rec = self.recipes.get_recipe_by_id(self.id)
        self.check_equal(self.recipe_name, rec.name)
        self.check_equal(self.recipe_text, rec.text)

    def check_set_text(self):
        new_text = 'brush potato, cut to pieces of 1-2 cm and boil for 20 minutes, then mash it thoroughly'
        self.recipes.set_text(self.id, new_text)
        rec = self.recipes.get_recipe_by_id(self.id)
        self.check_equal(new_text, rec.text)
        self.recipe_text = new_text

    def check_set_name(self):
        new_name = 'mashed potato'
        self.recipes.set_name(self.id, new_name)
        rec = self.recipes.get_recipe_by_id(self.id)
        self.check_equal(new_name, rec.name)
        self.recipe_name = new_name

    def check_delete_recipe(self):
        self.check_not_throws(self.recipes.get_recipe_by_id, self.id)
        self.delete_recipe()
        self.check_throws(self.recipes.get_recipe_by_id, self.id)

    def check(self):
        self.add_recipe()
        self.check_add_recipe()
        self.check_set_text()
        self.check_set_name()
        self.check_delete_recipe()
