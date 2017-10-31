import json
import logging
from psycopg2 import sql
from DBObject import DBObject


class Ingredient(DBObject):
    """Ingredient Class"""
    def __init__(self, recipe_id = -1):
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
        self.image = '{ "image" : ' + json.dumps(ingredient_json['image']) + '}'

    def populate_statement(self, conn):
        """update the database with object"""
        if self.id == -1:
            logging.error("First populate the fields")
            return -1
        # First check if this ingredient exists
        # query = sql.SQL("select {0} from {1}").format(
        # ...    sql.SQL(', ').join([sql.Identifier('foo'), sql.Identifier('bar')]),
        # ...    sql.Identifier('table'))
        cursor = conn.cursor()
        select_statement = sql.SQL("SELECT {0} FROM {1} where {2} = %s").format(sql.Identifier('recipes'),
                                                                                sql.Identifier('ingredients'),
                                                                                sql.Identifier('id'))
        cursor.execute(select_statement, [self.id])
        if cursor.rowcount > 0:
            # This ingredient exists, we'll have to update the recipe list
            j = cursor.fetchone()[0]
            j.append(self.recipe)
            self.statement = sql.SQL("""UPDATE {0} SET {1} = %s WHERE {2} = %s""").format(sql.Identifier('ingredients'),
                                                                                          sql.Identifier('recipes'),
                                                                                          sql.Identifier('id'))
            self.params = '[' + ', '.join(str(e) for e in j) + ']'
            self.params = [self.params, self.id]
        else:
            # Update a new ingredient
            recipes = '[' + str(self.recipe) + ']'
            self.statement = sql.SQL("INSERT INTO {0} VALUES (%s, %s, %s, %s, %s)").format(sql.Identifier('ingredients'))
            self.params = [self.id, self.name, self.type, self.image, recipes]
        cursor.close()
        return 0


    def populate_from_db(self, conn, obj_id):
        cursor = conn.cursor()
        select_statement = sql.SQL("SELECT * FROM {0} WHERE {1} = %s").format(sql.Identifier('ingredients'),
                                                                              sql.Identifier('id'))
        cursor.execute(select_statement, [obj_id])
        ing = cursor.fetchone()
        self.id = ing[0]
        self.name = ing[1]
        self.type = ing[2]
        self.image = ing[3]
        self.recipe = ing[4]
        return 0

    def get_recipe_count(self):
        if (self.id == -1 or type(self.recipe) != list):
            logging.error("Populate the Ingredient from the DB first! Call populate_from_db(ingredient_id)")
            return -1
        return len(self.recipe)



