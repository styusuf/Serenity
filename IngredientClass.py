import json
import logging
import traceback

class Ingredient:
    """Ingredient Class"""
    def __init__(self, recipe_id):
        self.id = -1
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

    def populate_from_db(self, cursor, ingredient_id):
        """populate the object from the database for ingredientID"""
        pass

    def update_db(self, conn):
        """update the database with object"""
        if self.id == -1:
            logging.error("First populate the fields")
            return -1
        # First check if this ingredient exists
        statement = None
        cursor = conn.cursor()
        select_statement = "SELECT recipes FROM ingredients where id = {}".format(self.id)
        cursor.execute(select_statement)
        if cursor.rowcount > 0:
            # This ingredient exists, we'll have to update the recipe list
            j = json.loads(cursor.fetchone()[0])
            j.append(self.recipe)
            statement = "UPDATE ingredients SET recipes = '{}' WHERE id = {}".format(j, self.id)
            pass
        else:
            # Update a new ingredient
            recipe = '\'[' + str(self.recipe) + ']\''
            statement = 'INSERT INTO ingredients VALUES ({}, {}, {}, {}, {}' \
                    ')'.format(self.id, self.name, self.type, self.image, recipe)
        try:
            cursor.execute(statement)
        except:
            e = traceback.format_exc()
            logging.error(e)
            return -1
        conn.commit()
        cursor.close()
        return 0

    def update_sql_file(self, filename):
        """update sql file with insert statement for this ingredient"""
        pass



