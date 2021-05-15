CREATE SEQUENCE violence_data_seq
    INCREMENT 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START 1
    CACHE 1;

CREATE TABLE type_violence(
  id numeric NOT NULL,
  name varchar(40),
  unique(id)
);

INSERT INTO type_violence (id, name) VALUES (1, 'Furtos');
INSERT INTO type_violence (id, name) VALUES (2, 'Roubo');
INSERT INTO type_violence (id, name) VALUES (3, 'Assalto a Grupo');
INSERT INTO type_violence (id, name) VALUES (4, 'Sequestro Relâmpago');
INSERT INTO type_violence (id, name) VALUES (5, 'Arrombamento Veicular');
INSERT INTO type_violence (id, name) VALUES (6, 'Arrombamento Domiciliar');
INSERT INTO type_violence (id, name) VALUES (9, 'Roubo de Veículo');
INSERT INTO type_violence (id, name) VALUES (10, 'Arrastão');
INSERT INTO type_violence (id, name) VALUES (11, 'Tentativa de Assalto');
INSERT INTO type_violence (id, name) VALUES (12, 'Tiroteio');

CREATE TABLE violence_data(
  id integer NOT NULL DEFAULT nextval('violence_data_seq'),
  title varchar(255),
  description TEXT,
  latitude numeric,
  longitude numeric, 
  type numeric REFERENCES type_violence(id),
  event_data timestamp,
  address varchar(255),
  icon varchar(255),
  county varchar(255),
  username varchar(255),
  name varchar(255),
  bulletin_occurrence varchar(255),
  damage_value numeric,
  neighborhood varchar(255),
  sex varchar(40),
  source varchar(40),
  day_of_week varchar(40),
  shift varchar(40)
);