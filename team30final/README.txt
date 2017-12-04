README for Serenity (Team 30)

Members: Aditya Sahai, Rachel Black, Samuel Yusuf, Ryan LaFleur

Part 1. Tour of Serenity Package
================================

Welcome to the README for Serenity (a.k.a. Fall 2017 CSE 6242 Team 30). At the top level
of this project (at the level this README file is at) contains only a few files.
These are mostly used to set up dependencies for the project, set up the database,
or to run the demo. You can read more about these in the following sections.

In the folder sql/ lives all the sql files for creating the database.

All the code for both the front-end and back-end lives in the app/ folder. The python
files for a lot of the back-end an front-end are in the first level of the app/ folder.
Specifically, DBInteract.py, DBObject.py mashape.py, and dbtest.py are how we interact with our posgres
database. IngredientClass.py, RawJson.py, RecipeClass.py are files for creating data
structures for the back-end. LookUpTables.py, IngredientCluster.py, and find_synonyms.py
manage data from the database and are used in back-end calculations. The core of
the backend computation is held in PredictQuery.py, QueryAdjuster.py (these 2 files
interact/create the machine learning model), and Ranking.py. Some of the front-end
to back-end handoff is handled by forms.py, views.py, and setup.py.

The other folders in app/ either store data or hold the front-end code. TestData holds
information that is used to populate our data structures and the machine learning
model. The folder named static/ holds the front-end code including all .js and .css
files as well as images/pages for displaying. The html templates are all held in templates/.

Part 2. Setting up the Project
==============================

To setup the project you need to install PostgreSQL. The project was build using PostgreSQL database version 10. Please look at the following to install postgres,

## Installing PostgreSQL10
### 1. Install from [PostgreSQL Website](https://www.postgresql.org/download/) (recommended)
  * This also installs pgAdmin GUI tool which makes using the database much easier.
  * Setup command line command **psql** by placing the following in your bash_profile (or equivalent)

      `alias psql="/Library/PostgreSQL/10/scripts/runpsql.sh"`

### 2. (Mac OSX) Install using [homebrew](https://launchschool.com/blog/how-to-install-postgresql-on-a-mac) 
  * Installs the `psql` tool by default


To populate the database, you'll have to make a few changes. If the name of the owner for the postgreSQL database is different than 'postgres', please edit the following lines in the database dump file in the "sql" folder (./sql/database_schema.sql),

  28:ALTER DATABASE fooddatabase OWNER TO postgres;
  75:ALTER TABLE ingredient_units OWNER TO postgres;
  91:ALTER TABLE ingredients OWNER TO postgres;
  104:ALTER TABLE people OWNER TO postgres;
  117:ALTER TABLE people_choices OWNER TO postgres;
  130:ALTER TABLE rawrecipejson OWNER TO postgres;
  156:ALTER TABLE recipes OWNER TO postgres;
  169:ALTER TABLE recipes_index OWNER TO postgres;

**(Please note that some of these tables like ingredient_units and recipes_index where only used for experimental purposes and are not used in application. We have decided to include them anyway to give a sense of the direction the application could be led into)**

Run the following commands,
1. `$ psql` (login using your username and password)
2. `# \i ./sql/database_schema.sql`

You also need to install the following python modules to make sure that the project runs, 

`$ pip install flask`
`$ pip install flask-login`
`$ pip install flask-openid`
`$ pip install flask-mail`
`$ pip install flask-sqlalchemy`
`$ pip install sqlalchemy-migrate`
`$ pip install flask-whooshalchemy`
`$ pip install flask-wtf`
`$ pip install flask-babel`
`$ pip install guess_language`
`$ pip install flipflop`
`$ pip install coverage`
`$ pip install psycopg2`
`$ pip install numpy`
`$ pip install sklearn`
`$ pip install unirest`

In order to populate the database, you need to run the ./app/mashape.py script. This script queries the Spoonacular API and get one recipe at a time. For each recipe, it populates the "recipes" table in the database, takes the ingredients out of the recipe object and populates the "ingredients" table. Spoonacular is a recipe database which has different membership types. We picked the cheapest plan which has a limit on the number of recipes we can query in a day. So, "mashape.py" populates only 5000 recipes at a time. You may have to create your own account on spoonalcular and update the key and host in mashape.py file (https://spoonacular.com/food-api). At this link you can select "Get Academic Access", fill out the questionnaire and you will recieve your Key and Host ID in your Email. Once you have created an account on Spoonacular, you'll be provided with a key and host which you can update in the mashape.py file at line numbers 29 and 30 respectively. 

NOTE: We haven't included any demo/toy data because all our machine learning models have been trained on a much larger dataset and they would break on toy data. The ranking mechanism also assumes that there are thousands of recipes.  

  27         response = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/random?limitLicense=false&number=1",
  28           headers={
  29             "X-Mashape-Key": "BuyjFV6xLqmshAVbK0ppDXmdXM0Jp1KsUhYjsnltPjvvB9mODp",
  30             "X-Mashape-Host": "spoonacular-recipe-food-nutrition-v1.p.mashape.com"
  31           }
  32         )

To run "mashape.py", 

`$ python mashape.py` 

Also, make the changes mentioned above in the file ./app/Ranking.py on the following line numbers. This will later enable you to run the application.

  94               headers={
  95                 "X-Mashape-Key": "BuyjFV6xLqmshAVbK0ppDXmdXM0Jp1KsUhYjsnltPjvvB9mODp",
  96                 "X-Mashape-Host": "spoonacular-recipe-food-nutrition-v1.p.mashape.com"
  97               }

Edit the login details to the database on line number 16 in mashape.py. This will enable you to login to the database successfully and edit it. Change the "user" to the <owner_name> described above, "password" to your password for that <owner_name> and "port" (usually 5432) attributes.

  14 def connect_to_db():
  15     try:
  16         return psql.connect("dbname='fooddatabase' user='<owner_name>' host='localhost' password='a' port='5433'")
  17     except:
  18         e = traceback.format_exc(0)
  19         print e
  20         print "unable to connect"
  21         exit(1)

Also make the same changes in line number 25 in ./app/DBInteract.py,

  25             self.conn = psql.connect("dbname='fooddatabase' user='<owner_name>' host='localhost' password='<owner_pass>' port='<port_number>'")

NOTE: If these values are wrong, you'll get the following error when you run the application in part 3.

*unable to connect*

Cleaning the Data using OpenRefine
----------------------------------
We had to do some cleaning to data and we used OpenRefine for this purpose. We cleaned the "unitLong" attribute of each ingredient and standardized the measuring unit for as many ingredients as possible to "ounces". For everything else, we query the Spoonacular API for a correct conversion value in the file Ranking.py (as discussed above). We have included the changes done in OpenRefine in the file OpenRefine.json. To use it, you must export the data in recipe table of the populated database to a file. Use the following command on the psql prompt, 

`# select id, ingredients from recipes \g path/to/file.txt`

and then use the included "ORjsonify.py" python script to convert this data into a json format which can be opened in OpenRefine.

`$ python ORjsonify.py path/to/input.txt path/to/output.json`

In OpenRefine you can use the OpenRefine.json file to apply the changes that we made after creating a project with the output.json file created above.

Part 3. Running the Demo
========================

You can check the demo.mov movie file to see a demo.

Please follow the following steps to run the application,

1. `$ python run.py` (run.py is in the base folder)
2. login to http://localhost:5000
3. On the UI, use the username password as follows, 
	username - admin
	password - password
4. Search for recipes!
