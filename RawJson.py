from DBObject import DBObject


class RawJson(DBObject):
    """Raw JSON Object"""
    def __init__(self, json_obj, recipe_id):
        DBObject.__init__(self)
        self.json = json_obj
        self.id = recipe_id

    def populate_statement(self):
        """Populate the statement for SQL"""
        self.statement = "INSERT INTO rawrecipejson VALUES ({}, '{}')"\
            .format(self.id, self.json)
