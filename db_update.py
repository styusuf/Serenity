import json
import psycopg2 as psql
from psycopg2 import sql

data = json.load(open('recipes.json'))

rows = data['rows']

recipes_list = dict()

for each in rows:
    ingredients = each
    recipe_id = ingredients.pop('recipe_id')
    try:
        recipes_list[recipe_id].append(ingredients)
    except KeyError:
        recipes_list[recipe_id] = list()
        recipes_list[recipe_id].append(ingredients)

print "number of reicpes = " + str(len(recipes_list))

try:
    conn = psql.connect("dbname='fooddatabase' user='postgres' host='localhost' password='a' port='5433'")
    for key in recipes_list.keys():
        try:
            id = int(key)
        except TypeError:
            print "what?"
        statement = sql.SQL("update {0} set {1} = %s where {2} = %s").format(sql.Identifier('recipes'),
                                                                 sql.Identifier('ingredients'),
                                                                 sql.Identifier('id'))
        with conn.cursor() as cursor:
            cursor.execute(statement, [json.dumps(recipes_list[key]), id])
finally:
    conn.commit()
    conn.close()