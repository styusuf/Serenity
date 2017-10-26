from DBObject import DBObject
from RawJson import RawJson
from IngredientClass import Ingredient
import logging
import json


class Recipe(DBObject):
    """Recipe Class"""
    def __init__(self):
        # Database entries
        DBObject.__init__(self)
        self.isVeg = None
        self.isVegan = None
        self.isGlutenFree = None
        self.isDairyFree = None
        self.title = None
        self.ReadyInMin = None
        self.CookingMin = None
        self.pricePerServing = None
        self.servings = None
        self.spoonacularScore = None
        self.image = None
        self.dishTypes = None
        self.instructions = None
        self.ingredients = None
        self.preparedInsertStatement = False
        # Ingredients JSON
        self.ingredientsJson = None
        # Raw Json
        self.rawJson = None

    def populate_from_json(self, json_object):
        """Feed the recipe json here and it will populate the fields"""
        recipe = json_object['recipes'][0]
        # Populate fields
        self.id = recipe['id']
        self.isVeg = recipe['vegetarian']
        self.isVegan = recipe['vegan']
        self.isGlutenFree = recipe['glutenFree']
        self.isDairyFree = recipe['dairyFree']
        self.title = json.dumps(recipe['title']).replace('\"', '\'')
        self.ReadyInMin = recipe['readyInMinutes']
        self.CookingMin = recipe['cookingMinutes']
        self.pricePerServing = recipe['pricePerServing']
        self.servings = recipe['servings']
        self.spoonacularScore = recipe['spoonacularScore']
        self.image = '\'{ "image" : "' + recipe['image'] + '"}\''
        self.dishTypes = '\'' + json.dumps(recipe['dishTypes']) + '\''

        # Instructions
        instructions_steps = recipe['analyzedInstructions'][0]['steps']
        for step in instructions_steps:
            step.pop('ingredients', None)
            step.pop('equipment', None)

        # Format of instructions
        # [ { step : ...
        #     number: ...
        #   },...]
        self.instructions = '\'' + json.dumps(instructions_steps) + '\''

        # Ingredients
        self.ingredientsJson = recipe['extendedIngredients']
        for i in self.ingredientsJson:
            i.pop('originalString', None)
            i.pop('metaInformation', None)
            i.pop('consistency', None)

        self.ingredients = '\'' + json.dumps(recipe['extendedIngredients']) + '\''

        # Raw Json
        self.rawJson = RawJson(json.dumps(json_object), self.id)

    def update_with_recipe(self, conn, filename):
        """Update the database with the recipe and ingredients"""
        if self.update_db(conn) != 0:
            logging.error("DB Update for recipe {} failed!".format(self.id))
        logging.info("Updated Recipe {}".format(self.id))

        # Update SQL file with recipe
        self.update_sql_file(filename)

        # Update Ingredients Table
        for i in self.ingredientsJson:
            ingr = Ingredient(self.id)
            ingr.populate_from_json(i)
            if (ingr.populate_statement(conn) & ingr.update_db(conn)) != 0:
                logging.error("Update for ingredient {} for recipe {} failed".format(ingr.id, self.id))
                return -1
            ingr.update_sql_file(filename)
        logging.info("Updated Ingredients for {}".format(self.id))

        # Update RawJson
        self.rawJson.populate_statement()
        if self.rawJson.update_db(conn) != 0:
            logging.error("DB update for raw json failed for recipe {} failed".format(self.id))
            return -1
        self.rawJson.update_sql_file(filename)
        logging.info("DB Update for raw json successful for recipe {}".format(self.id))
        return 0

    def populate_insert_statement(self):
        """Populate the insert statement"""
        if self.id == -1:
            logging.error("First populate the fields")
            return -1
        self.statement = 'INSERT INTO recipes VALUES ( {}, {}, {}, {}, {},'\
              '{}, {}, {}, {}, {}, ' \
              '{}, {}, {}, {}, {})'.format(self.id, self.isVeg, self.isVegan,
              self.isGlutenFree, self.isDairyFree, self.title, self.ReadyInMin,
              self.CookingMin, self.pricePerServing, self.servings, self.spoonacularScore,
              self.image, self.dishTypes, self.instructions, self.ingredients)
        self.preparedInsertStatement = True
        return 0
