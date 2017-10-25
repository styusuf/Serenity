DROP DATABASE IF EXISTS foodtest;

CREATE DATABASE foodtest
	WITH
	OWNER = postgres
	ENCODING = 'UTF8'
	TABLESPACE = pg_default
	CONNECTION LIMIT = -1;

-- Postgres command
\c foodtest;

drop table if exists recipes;
drop table if exists ingredients;
drop type if exists ingredient_type;

create table recipes (
	id serial NOT NULL,
	instructions jsonb,
	ingredients jsonb,
	image jsonb,
	PRIMARY KEY(id)
);

create type ingredient_type as ENUM ('spices', 'meats');

create table ingredients (
	id serial NOT NULL,
	type ingredient_type,
	image jsonb,
	recipes json,
	PRIMARY KEY(id)
);