import psycopg2 as psql
import json

try:
	conn = psql.connect("dbname='foodtest' user='postgres' host='localhost' password='a' port='5433'")
except:
	print "unable to connect"

# Open file
with open('sample.json') as data_file:
	data = json.load(data_file)



