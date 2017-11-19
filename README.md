# Team-Serenity
Data and Visual analytics project

## Installing PostgreSQL10
### 1. Install from [PostgreSQL Website](https://www.postgresql.org/download/) (recommended)
  * This also installs pgAdmin GUI tool which makes using the database much easier.
  * Setup command line command **psql** by placing the following in your bash_profile (or equivalent)

      `alias psql="/Library/PostgreSQL/10/scripts/runpsql.sh"`
### 2. (Mac OSX) Install using [homebrew](https://launchschool.com/blog/how-to-install-postgresql-on-a-mac) 
  * Installs the `psql` tool by default
  
  
## [PSQL Cheatsheet](http://www.postgresonline.com/downloads/special_feature/postgresql83_psql_cheatsheet.pdf)

## PSQL interactive console commands usefuls in our project
  * \l (list databases)
  * \c (connect to database)
  * \i </path/to/script> (Run script)
  * \d (list tables in database)
  
 ## [Git Bash for Windows](https://git-for-windows.github.io/)
  
 ## [Git Cheatsheet](https://education.github.com/git-cheat-sheet-education.pdf)
 
 ## Python tools
 
* ### [Install psycopg2](http://initd.org/psycopg/docs/install.html)
 
* ### [Install unirest](http://unirest.io/python.html)

* ## To work with Flask
`
$ flask/bin/pip install flask
$ flask/bin/pip install flask-login
$ flask/bin/pip install flask-openid
$ flask/bin/pip install flask-mail
$ flask/bin/pip install flask-sqlalchemy
$ flask/bin/pip install sqlalchemy-migrate
$ flask/bin/pip install flask-whooshalchemy
$ flask/bin/pip install flask-wtf
$ flask/bin/pip install flask-babel
$ flask/bin/pip install guess_language
$ flask/bin/pip install flipflop
$ flask/bin/pip install coverage
`