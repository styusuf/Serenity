DROP DATABASE IF EXISTS FoodDatabase;

CREATE DATABASE FoodDatabase
	WITH
	OWNER = postgres
	ENCODING = 'UTF8'
	TABLESPACE = pg_default
	CONNECTION LIMIT = -1;

-- Postgres command
\c fooddatabase

drop table if exists recipes;
drop table if exists ingredients;

create table recipes (
	id int NOT NULL,
	veg boolean NOT NULL, 
	vegan boolean NOT NULL,
	glutenFree boolean NOT NULL,
	dairyFree boolean NOT NULL,
	title varchar(256) NOT NULL,
	ReadyInMin int NOT NULL,
	CookingMin int NOT NULL,
	pricePerServing numeric NOT NULL,
	servings int NOT NULL, 
	spoonacularScore int NOT NULL,
	image jsonb,
	dishTypes jsonb,
	instructions jsonb,
	ingredients jsonb,
	PRIMARY KEY(id)
);

create table ingredients (
	id int NOT NULL,
	name varchar(256) NOT NULL,
	type varchar(256) NOT NULL,
	image jsonb,
	recipes json,
	PRIMARY KEY(id)
);

create table rawrecipejson (
	id int NOT NULL,
	object jsonb,
	PRIMARY KEY(id)
);