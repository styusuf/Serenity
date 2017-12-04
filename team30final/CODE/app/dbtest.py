import psycopg2 as psql
import json
from IngredientClass import Ingredient
from RecipeClass import Recipe
from IngredientClass import Ingredient

# psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
# psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

conn = None

try:
	conn = psql.connect("dbname='fooddatabaseverify' user='postgres' host='localhost' password='a' port='5433'")
except:
	print "unable to connect"
	exit(1)

ingr = Ingredient()
if (ingr.populate_from_db(conn, 98913) != 0):
    print "Error pulling ingredient data"
    exit(1)

print ingr.id
print ingr.name
print ingr.get_recipe_count()

rec = Recipe()
if (rec.populate_from_db(conn, 590007) != 0):
    print "Error pull recipe data"
    exit(1)
print rec.id
print rec.title

i = Ingredient(1234)
i.id = 1007
i.populate_statement(conn)
c = conn.cursor()
c.execute(i.statement, i.params)
conn.commit()
c.close()
conn.close()

