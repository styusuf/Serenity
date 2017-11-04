import traceback
import psycopg2 as psql
from psycopg2 import sql


class DBInteract(object):
    '''
    Class to interact with the DB. All DB functions to be written here.
    '''
    def __init__(self):
        self.conn = None
        self.recipe = sql.Identifier('recipes')
        self.ingredient = sql.Identifier('ingredients')
        self.id = sql.Identifier('id')

    def connect_to_db(self):
        '''
        Class to connect to the DB
        :return: None
        '''
        try:
            self.conn = psql.connect("dbname='fooddatabase' user='postgres' host='localhost' password='a' port='5433'")
        except:
            e = traceback.format_exc(0)
            print e
            print "unable to connect"
            exit(1)

    def get_recipe_count(self, ingredient_id):
        '''
        Get the count of all recipes for given ingredient
        :param ingredient_id:
        :return: Integer
        '''
        self.connect_to_db()
        statement = sql.SQL("SELECT json_array_length({0}) from {1} where {2} = %s").format(self.recipe,
                                                                                        self.ingredient, self.id)
        cursor = self.conn.cursor()
        cursor.execute(statement, [ingredient_id])
        rec_count = cursor.fetchone()[0]
        cursor.close()
        self.conn.close()
        return rec_count

    def get_recipes(self, ingredients_list):
        '''
        Get the list of all common recipes for the list of ingredients
        :param ingredients_list: list of ingredients
        :return: list of recipes
        '''
        self.connect_to_db()
        statement = sql.SQL("SELECT {0} FROM {1} WHERE {2} IN (" + "%s," * (len(ingredients_list) - 1)  + "%s)")\
                                                                            .format(self.recipe, self.ingredient, self.id)
        cursor = self.conn.cursor()
        cursor.execute(statement, ingredients_list)
        recipes = set()
        for each in cursor.fetchall():
            for r in each[0]:
                recipes.add(r)
        cursor.close()
        self.conn.close()
        return list(recipes)

    def get_recipe_total(self):
        '''
        get the count of all recipes in the database
        :return: Integer
        '''
        self.connect_to_db()
        statement = sql.SQL("SELECT COUNT(*) FROM {0}").format(self.recipe)
        cursor = self.conn.cursor()
        cursor.execute(statement)
        count = cursor.fetchone()[0]
        cursor.close()
        self.conn.close()
        return count


if __name__ == '__main__':
    dbi = DBInteract()
    print dbi.get_recipe_count(2047)

