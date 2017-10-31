import traceback
import psycopg2 as psql
from psycopg2 import sql
import sys


def connect_to_db():
    try:
        return psql.connect("dbname='fooddatabase' user='postgres' host='localhost' password='a' port='5433'")
    except:
        e = traceback.format_exc(0)
        print e
        print "unable to connect"
        exit(1)

def get_recipes(ingredient_list):
    conn = connect_to_db()
    statement = sql.SQL("SELECT {0} FROM {1} WHERE {2} IN (" + "%s," * (len(ingredient_list) - 1)  + "%s)").format(sql.Identifier('recipes'),
                                                                            sql.Identifier('ingredients'),
                                                                            sql.Identifier('id'))
    cursor = conn.cursor()
    cursor.execute(statement, ingredient_list)
    recipes = set()
    for each in cursor.fetchall():
        for r in each[0]:
            recipes.add(r)
    cursor.close()
    conn.close()
    return list(recipes)


def main(argv):
    get_recipes(argv)

if __name__ == '__main__':
    main(sys.argv[1:])


