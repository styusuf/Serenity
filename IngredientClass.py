import json
import logging
from psycopg2 import sql
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

