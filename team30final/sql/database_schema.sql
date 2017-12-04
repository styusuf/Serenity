--
-- PostgreSQL database dump
--

-- Dumped from database version 10.0
-- Dumped by pg_dump version 10.0

-- Started on 2017-12-03 16:34:11 EST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE fooddatabase;
--
-- TOC entry 3159 (class 1262 OID 24729)
-- Name: fooddatabase; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE fooddatabase WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'C' LC_CTYPE = 'C';


ALTER DATABASE fooddatabase OWNER TO postgres;

\connect fooddatabase

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 1 (class 3079 OID 13241)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 3162 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 202 (class 1259 OID 191658)
-- Name: ingredient_units; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE ingredient_units (
    id text,
    units json
);


ALTER TABLE ingredient_units OWNER TO postgres;

--
-- TOC entry 197 (class 1259 OID 24738)
-- Name: ingredients; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE ingredients (
    id integer NOT NULL,
    name character varying(256) NOT NULL,
    type character varying(256) NOT NULL,
    image jsonb,
    recipes json
);


ALTER TABLE ingredients OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 182648)
-- Name: people; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE people (
    username character varying(256) NOT NULL,
    password character varying(256)
);


ALTER TABLE people OWNER TO postgres;

--
-- TOC entry 201 (class 1259 OID 182656)
-- Name: people_choices; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE people_choices (
    username character varying(256) NOT NULL,
    recipes json
);


ALTER TABLE people_choices OWNER TO postgres;

--
-- TOC entry 198 (class 1259 OID 24746)
-- Name: rawrecipejson; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE rawrecipejson (
    id integer NOT NULL,
    object jsonb
);


ALTER TABLE rawrecipejson OWNER TO postgres;

--
-- TOC entry 196 (class 1259 OID 24730)
-- Name: recipes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE recipes (
    id integer NOT NULL,
    veg boolean NOT NULL,
    vegan boolean NOT NULL,
    glutenfree boolean NOT NULL,
    dairyfree boolean NOT NULL,
    title character varying(256) NOT NULL,
    readyinmin integer NOT NULL,
    cookingmin integer NOT NULL,
    priceperserving numeric NOT NULL,
    servings integer NOT NULL,
    spoonacularscore integer NOT NULL,
    image jsonb,
    dishtypes jsonb,
    instructions jsonb,
    ingredients jsonb
);


ALTER TABLE recipes OWNER TO postgres;

--
-- TOC entry 199 (class 1259 OID 182549)
-- Name: recipes_index; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE recipes_index (
    id integer,
    ingredients json
);


ALTER TABLE recipes_index OWNER TO postgres;


ALTER TABLE ONLY ingredients
    ADD CONSTRAINT ingredients_pkey PRIMARY KEY (id);


--
-- TOC entry 3025 (class 2606 OID 182663)
-- Name: people_choices people_choices_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY people_choices
    ADD CONSTRAINT people_choices_pkey PRIMARY KEY (username);


--
-- TOC entry 3023 (class 2606 OID 182655)
-- Name: people people_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY people
    ADD CONSTRAINT people_pkey PRIMARY KEY (username);


--
-- TOC entry 3021 (class 2606 OID 24753)
-- Name: rawrecipejson rawrecipejson_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY rawrecipejson
    ADD CONSTRAINT rawrecipejson_pkey PRIMARY KEY (id);


--
-- TOC entry 3017 (class 2606 OID 24737)
-- Name: recipes recipes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY recipes
    ADD CONSTRAINT recipes_pkey PRIMARY KEY (id);


--
-- TOC entry 3026 (class 2606 OID 182664)
-- Name: people_choices people_choices_username_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY people_choices
    ADD CONSTRAINT people_choices_username_fkey FOREIGN KEY (username) REFERENCES people(username) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3161 (class 0 OID 0)
-- Dependencies: 5
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2017-12-03 16:34:23 EST

--
-- PostgreSQL database dump complete
--

