import psycopg2 as psql
import json

conn = None

try:
	conn = psql.connect("dbname='foodtest' user='postgres' host='localhost' password='a' port='5433'")
except:
	print "unable to connect"
	exit(1)

# Open file
with open('sample.json') as data_file:
	data = json.load(data_file)


# ingredients = str(data['ingredients']).replace('u\'', '"').replace('\'', '"')
ingredients = json.dumps(data['ingredients'])
# print ingredients

# insert_command = "insert into recipes (ingredients) values ('" + ingredients + "')"

if conn:
    cursor = conn.cursor()
    cursor.execute("select * from recipes;")
    print cursor.fetchall()
    cursor.execute("INSERT INTO recipes (ingredients) values('" + ingredients + "')")
    conn.commit()
    cursor.execute("select * from recipes;")
    print cursor.fetchall()