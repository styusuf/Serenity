from IngredientClass import Ingredient
import logging
import json
import traceback



class Recipe:
    """Recipe Class"""
    def __init__(self):
        # Database entries
        self.id = -1
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
        # Insert statement
        self.insertStatement = None
        self.preparedInsertStatement = False
        # Ingredients JSON
        self.ingredientsJson = None

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

    def update_db(self, conn):
        """Update the database with the recipe and ingredients"""
        if self.preparedInsertStatement == False:
            self.populate_insert_statement()
        cursor = conn.cursor()
        try:
            cursor.execute(self.insertStatement)
        except:
            e = traceback.format_exc()
            logging.error(e)
            return -1
        conn.commit()
        cursor.close()
        logging.info("Updated Recipe {}".format(self.id))
        # Update Ingredients Table
        for i in self.ingredientsJson:
            ingr = Ingredient(self.id)
            ingr.populate_from_json(i)
            ingr.update_db(conn)
        return 0


    def populate_from_db(self, conn, recipe_id):
        """Update the object from the database cursor and id"""
        pass

    def update_sql_file(self, filename):
        """update sql file with insert statement for this recipe"""
        pass

    def populate_insert_statement(self):
        """Populate the insert statement"""
        if self.id == -1:
            logging.error("First populate the fields")
            return -1
        self.insertStatement = 'INSERT INTO recipes VALUES ( {}, {}, {}, {}, {}, ' \
                '{}, {}, {}, {}, {}, ' \
                '{}, {}, {}, {}, {})'.format(self.id, self.isVeg, self.isVegan,
                    self.isGlutenFree, self.isDairyFree, self.title, self.ReadyInMin,
                    self.CookingMin, self.pricePerServing, self.servings, self.spoonacularScore,
                    self.image, self.dishTypes, self.instructions, self.ingredients)
        self.preparedInsertStatement = True
        return 0

