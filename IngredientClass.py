import json
import logging

class Ingredient:
    """Ingredient Class"""
    def __init__(self, recipe_id):
        self.id = None
        self.name = None
        self.type = None
        self.image = None
        self.recipe = recipe_id

    def populate_from_json(self, ingredient_json):
        """populate object from json"""
        self.id = ingredient_json['id']
        self.name = ingredient_json['name']
        self.type = ingredient_json['aisle']
        self.image = '{ "image" : "' + json.dumps(ingredient_json['image']) + '"}'

    def populate_from_db(self, cursor, ingredient_id):
        """populate the object from the database for ingredientID"""
        pass

    def update_db(self, cursor):
        """update the database with object"""
        pass

    def update_sql_file(self, filename):
        """update sql file with insert statement for this ingredient"""
        pass



