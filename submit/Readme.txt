README for Serenity

Members: Aditya Sahai, Rachel Black, Samuel Yusuf, Ryan LaFleur

Part 1. Tour of Serenity Package

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
To setup the project you need to install PostgreSQL. The project was build using PostgreSQL database version 10. Please look at the following to install postgres,

## Installing PostgreSQL10
### 1. Install from [PostgreSQL Website](https://www.postgresql.org/download/) (recommended)
  * This also installs pgAdmin GUI tool which makes using the database much easier.
  * Setup command line command **psql** by placing the following in your bash_profile (or equivalent)

      `alias psql="/Library/PostgreSQL/10/scripts/runpsql.sh"`

### 2. (Mac OSX) Install using [homebrew](https://launchschool.com/blog/how-to-install-postgresql-on-a-mac) 
  * Installs the `psql` tool by default


To populate the database, you'll have to make a few changes. If the name of the owner for the postgreSQL database is different than 'postgres', please edit the following lines in the database dump file in the "sql" folder (./sql/database_dump.sql),

28:ALTER DATABASE fooddatabase OWNER TO <owner_name>;
75:ALTER TABLE ingredient_units OWNER TO <owner_name>;
91:ALTER TABLE ingredients OWNER TO <owner_name>;
104:ALTER TABLE people OWNER TO <owner_name>;
117:ALTER TABLE people_choices OWNER TO <owner_name>;
130:ALTER TABLE rawrecipejson OWNER TO <owner_name>;
156:ALTER TABLE recipes OWNER TO <owner_name>;
169:ALTER TABLE recipes_index OWNER TO <owner_name>;

**(Please note that some of these tables like ingredient_units and recipes_index where only used for experimental purposes and are not used in application. We have decided to include them anyway to give a sense of the direction the application could be led into)**

Run the following commands,
1. `$ psql` (login using your username and password)
2. `# \i ./sql/database_dump.sql` (this step might take a few minutes)

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
`$ pip install sklearn`
`$ pip install numpy`

You also need to edit the login details in the following file/line number to make sure that the python application is able to connect to the database,
* In the file ./app/DBInteract.py, make changes on line number 25. Change the "user" to the <owner_name> described above, "password" to your password for that <owner_name> and "port" (usually 5432) attributes.

  25             self.conn = psql.connect("dbname='fooddatabase' user='<owner_name>' host='localhost' password='<owner_pass>' port='<port_number>'")

If these values are wrong, you'll get the following error when you run the application in part 3.

*unable to connect*

Part 3. Running the Demo

Please follow the following steps to run the application

1. `$ python run.py` (run.py is in the base folder)
2. login to http://localhost:5000
3. On the UI, use the username password as follows, 
	username - admin
	password - password
4. Search for recipes!
