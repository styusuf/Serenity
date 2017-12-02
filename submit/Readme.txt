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

Part 3. Running the Demo
