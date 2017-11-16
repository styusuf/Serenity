from DBObject import DBObject
from RawJson import RawJson
from IngredientClass import Ingredient
from psycopg2 import sql
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
        logging.error("Populating for recipe id = " + str(self.id))
        self.isVeg = recipe['vegetarian']
        self.isVegan = recipe['vegan']
        self.isGlutenFree = recipe['glutenFree']
        self.isDairyFree = recipe['dairyFree']
        self.title = json.dumps(recipe['title']).replace('\"', '\'')
        self.ReadyInMin = recipe['readyInMinutes']
        try:
            self.CookingMin = recipe['cookingMinutes']
        except KeyError:
            self.CookingMin = 0
        self.pricePerServing = recipe['pricePerServing']
        self.servings = recipe['servings']
        self.spoonacularScore = recipe['spoonacularScore']
        self.image = '{ "image" : ' + json.dumps(recipe['image']) + '}'
        self.dishTypes = json.dumps(recipe['dishTypes'])

        # Instructions
        try:
            instructions_steps = recipe['analyzedInstructions'][0]['steps']
            for step in instructions_steps:
                step.pop('ingredients', None)
                step.pop('equipment', None)
        except IndexError:
            instructions_steps = recipe['instructions']


        # Format of instructions
        # [ { step : ...
        #     number: ...
        #   },...]
        self.instructions = json.dumps(instructions_steps)

        # Ingredients
        self.ingredientsJson = recipe['extendedIngredients']
        for i in self.ingredientsJson:
            i.pop('originalString', None)
            i.pop('metaInformation', None)
            i.pop('consistency', None)

        self.ingredients = json.dumps(recipe['extendedIngredients'])

        # Raw Json
        self.rawJson = RawJson(json.dumps(json_object), self.id)

    def update_with_recipe(self, conn, filename):
        # Update SQL file with recipe
        """Update the database with the recipe and ingredients"""
        if self.update_db(conn) != 0:
            logging.error("DB Update for recipe {} failed!".format(self.id))
            return -1
        logging.info("Updated Recipe {}".format(self.id))
        self.update_sql_file(filename, conn)

        # Update Ingredients Table
        for i in self.ingredientsJson:
            ingr = Ingredient(self.id)
            ingr.populate_from_json(i)
            if (ingr.populate_statement(conn) & ingr.update_db(conn)) != 0:
                logging.error("Update for ingredient {} for recipe {} failed".format(ingr.id, self.id))
                return -1
            if ingr.update_sql_file(filename, conn) == 0:
                logging.info("Ingredient statement updated in SQL file")
            else:
                logging.error("Ingredient statement update in SQL file failed")
        logging.info("Updated Ingredients for {}".format(self.id))

        # Update RawJson
        self.rawJson.populate_statement()
        if self.rawJson.update_sql_file(filename, conn) == 0:
            logging.info("raw json statement updated in SQL file")
        else:
            logging.error("raw json statement update in SQL file failed")

        if self.rawJson.update_db(conn) != 0:
            logging.error("DB update for raw json failed for recipe {} failed".format(self.id))
            return -1
        logging.info("DB Update for raw json successful for recipe {}".format(self.id))
        return 0

    def populate_insert_statement(self, conn):
        """Populate the insert statement"""
        if self.id == -1:
            logging.error("First populate the fields")
            return -1
        self.statement = sql.SQL("""INSERT INTO {0} VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""").format(sql.Identifier('recipes'))
        self.params = [self.id, self.isVeg, self.isVegan,
              self.isGlutenFree, self.isDairyFree, self.title, self.ReadyInMin,
              self.CookingMin, self.pricePerServing, self.servings, self.spoonacularScore,
              self.image, self.dishTypes, self.instructions, self.ingredients]
        self.preparedInsertStatement = True
        return 0

    def populate_from_db(self, conn, obj_id):
        cursor = conn.cursor()
        select_statement = sql.SQL("SELECT * FROM {0} WHERE {1} = %s").format(sql.Identifier('recipes'),
                                                                              sql.Identifier('id'))
        cursor.execute(select_statement, [obj_id])
        rec = cursor.fetchone()
        self.populate(rec)
        return 0

    def populate(self, rec):
        self.id = rec[0]
        self.isVeg = rec[1]
        self.isVegan = rec[2]
        self.isGlutenFree = rec[3]
        self.isDairyFree = rec[4]
        self.title = rec[5]
        self.ReadyInMin = rec[6]
        self.CookingMin = rec[7]
        self.pricePerServing = rec[8]
        self.servings = rec[9]
        self.spoonacularScore = rec[10]
        self.image = rec[11]
        self.dishTypes = rec[12]
        self.instructions = rec[13]
        self.ingredients = rec[14]





