from DBObject import DBObject
from psycopg2 import sql

class RawJson(DBObject):
    """Raw JSON Object"""
    def __init__(self, json_obj, recipe_id):
        DBObject.__init__(self)
        self.json = json_obj
        self.id = recipe_id

    def populate_statement(self):
        """Populate the statement for SQL"""
        self.statement = sql.SQL("INSERT INTO {0} VALUES (%s, %s)").format(sql.Identifier('rawrecipejson'))
        self.params = [self.id, self.json]

