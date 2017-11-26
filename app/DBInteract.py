import traceback
import psycopg2 as psql
from psycopg2 import sql
from RecipeClass import Recipe

class DBInteract(object):
    '''
    Class to interact with the DB. All DB functions to be written here.
    '''
    def __init__(self):
        self.conn = None
        self.recipe = sql.Identifier('recipes')
        self.ingredient = sql.Identifier('ingredients')
        self.people = sql.Identifier('people')
        self.password = sql.Identifier('password')
        self.username = sql.Identifier('username')
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

    def get_password(self, username):
        '''
        Get the password for the given username
        :param username:
        :return:
        '''
        self.connect_to_db()
        statement = sql.SQL("SELECT {0} from {1} WHERE {2} = %s").format(self.password,
                                                                         self.people,
                                                                         self.username)
        with self.conn.cursor() as cursor:
            cursor.execute(statement, [username])
            if cursor.rowcount > 0:
                password = cursor.fetchone()[0]
            else:
                password = None
        self.conn.close()
        return password

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

    def get_recipes_verbose(self, recipe_list):
        self.connect_to_db()
        statement = sql.SQL("SELECT * FROM {0} WHERE {1} IN (" + "%s," * (len(recipe_list) - 1) + "%s)")\
                                                                            .format(self.recipe, self.id)
        cursor = self.conn.cursor()
        cursor.execute(statement, recipe_list)
        recipe_object_list = list()
        for each in cursor.fetchall():
            r = Recipe()
            r.populate(each)
            recipe_object_list.append(r)

        cursor.close()
        self.conn.close()
        return recipe_object_list

    def get_recipes(self, ingredients_list, verbose=False):
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
        flag = False
        for each in cursor.fetchall():
            if not flag:
                recipes = set(each[0])
                flag = True
            else:
                recipes = recipes.intersection(each[0])

        cursor.close()
        self.conn.close()
        if not verbose:
            return list(recipes)
        else:
            if len(list(recipes)) > 0:
                return self.get_recipes_verbose(list(recipes))
            else:
                return list()

    def get_recipes_with_synonyms(self, ingredients_list, ingredient_info, group_info, verbose=False):
        """
        Get the list of all common recipes for the list of ingredients using synonyms
        :param ingredients_list: list of ingredients
        :param verbose: Option to use print statements
        :return: list of recipes
        """
        self.connect_to_db()

        search_str_builder = []
        for ingredient in ingredients_list:
            new_or_statement_builder = []
            for grp in ingredient_info[ingredient]["group"]:
                for syn in group_info[grp]["ingredient list"]:
                    new_or_statement_builder.append("ingredients::jsonb @> '[{}]'::jsonb".format(syn))
            search_str_builder.append("(" + " OR ".join(new_or_statement_builder) + ")")
        search_str = " AND ".join(search_str_builder) + ";"
        statement = sql.SQL("SELECT id FROM recipes_index WHERE {}".format(search_str))

        cursor = self.conn.cursor()
        cursor.execute(statement)
        recipes = [x[0] for x in cursor.fetchall()]

        cursor.close()
        self.conn.close()
        if not verbose:
            return list(recipes)
        else:
            if len(list(recipes)) > 0:
                return self.get_recipes_verbose(list(recipes))
            else:
                return list()

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
    # print dbi.get_recipe_count(2047)
    a = dbi.get_recipes([16117], verbose=False)
    # print a[0].instructions
    print a
