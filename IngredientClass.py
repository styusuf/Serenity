import json
import logging
from DBObject import DBObject


class Ingredient(DBObject):
    """Ingredient Class"""
    def __init__(self, recipe_id):
        DBObject.__init__(self)
        self.name = None
        self.type = None
        self.image = None
        self.recipe = recipe_id

    def populate_from_json(self, ingredient_json):
        """populate object from json"""
        self.id = ingredient_json['id']
        self.name = json.dumps(ingredient_json['name']).replace('\"', '\'')
        self.type = json.dumps(ingredient_json['aisle']).replace('\"', '\'')
        self.image = '\'{ "image" : ' + json.dumps(ingredient_json['image']) + '}\''

    def populate_statement(self, conn):
        """update the database with object"""
        if self.id == -1:
            logging.error("First populate the fields")
            return -1
        # First check if this ingredient exists
        cursor = conn.cursor()
        select_statement = "SELECT recipes FROM ingredients where id = {}".format(self.id)
        cursor.execute(select_statement)
        if cursor.rowcount > 0:
            # This ingredient exists, we'll have to update the recipe list
            j = json.loads(cursor.fetchone()[0])
            j.append(self.recipe)
            self.statement = "UPDATE ingredients SET recipes = '{}' WHERE id = {}".format(j, self.id)
            pass
        else:
            # Update a new ingredient
            recipe = '\'[' + str(self.recipe) + ']\''
            self.statement = 'INSERT INTO ingredients VALUES ({}, {}, {}, {}, {})'\
                .format(self.id, self.name, self.type, self.image, recipe)
        cursor.close()
        return 0

