import psycopg2 as psql
import json
from RecipeClass import Recipe

conn = None

try:
	conn = psql.connect("dbname='fooddatabase' user='postgres' host='localhost' password='a' port='5433'")
except:
	print "unable to connect"
	exit(1)

# Open file
with open('sample.json') as data_file:
	data = json.load(data_file)

a = Recipe()
a.populate_from_json(data)
a.populate_insert_statement()
print a.insertStatement

cursor = conn.cursor()

cursor.execute(a.insertStatement)
conn.commit()

