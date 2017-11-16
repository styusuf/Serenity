import unirest
import re
import datetime
from ssl import SSLError
import json
import traceback
import logging
import psycopg2 as psql
from RecipeClass import Recipe

# psql.extensions.register_type(psql.extensions.UNICODE)
# psql.extensions.register_type(psql.extensions.UNICODEARRAY)

def connect_to_db():
    try:
        return psql.connect("dbname='fooddatabase' user='postgres' host='localhost' password='a' port='5433'")
    except:
        e = traceback.format_exc(0)
        print e
        print "unable to connect"
        exit(1)

for i in range(1,4000):
    print "{} requests".format(i)
    try:
        unirest.timeout(10)
        response = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/random?limitLicense=false&number=1",
          headers={
            "X-Mashape-Key": "BuyjFV6xLqmshAVbK0ppDXmdXM0Jp1KsUhYjsnltPjvvB9mODp",
            "X-Mashape-Host": "spoonacular-recipe-food-nutrition-v1.p.mashape.com"
          }
        )
        filename = 'json_objects/{}.json'.format(re.sub(r'[-:. ]', '', str(datetime.datetime.now())))
        # a = json.loads(response.body);
        data = json.loads(response.raw_body)

        # Update local file with json
        with open(filename, 'w') as f:
            f.write(str(response.raw_body))

        conn = connect_to_db()

        sqlfilename = 'master_' + str(datetime.date.today()).replace('-', '') + '.sql'
        a = Recipe()
        a.populate_from_json(data)
        a.populate_insert_statement(conn)
        
        if a.update_with_recipe(conn, sqlfilename) == 0:
            print "success"
            conn.commit()
            conn.close()
        else:
            conn.close()
            print "fail"
    
    except SSLError:
        conn.close()
        print "SSL ERROR"
        continue
    except:
        e = traceback.format_exc(5)
        logging.error(e)
        conn.close()
        print "Skipping this recipe"
        continue

