import unirest
import re
import datetime
from ssl import SSLError

for i in range(1,3001):
    print "{} requests".format(i)
    try:
        response = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/random?limitLicense=false&number=1",
          headers={
            "X-Mashape-Key": "BuyjFV6xLqmshAVbK0ppDXmdXM0Jp1KsUhYjsnltPjvvB9mODp",
            "X-Mashape-Host": "spoonacular-recipe-food-nutrition-v1.p.mashape.com"
          }
        )
        filename = 'json_objects/{}.json'.format(re.sub(r'[-:. ]', '', str(datetime.datetime.now())))
        with open(filename, 'w') as f:
            f.write(str(response.body))
    except SSLError:
        print "SSL ERROR"

