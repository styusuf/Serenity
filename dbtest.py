import psycopg2 as psql
import json
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


i = Ingredient(1234)
i.id = 1007
i.populate_statement(conn)
c = conn.cursor()
c.execute(i.statement, i.params)
conn.commit()
c.close()
conn.close()