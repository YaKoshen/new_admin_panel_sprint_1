-- DROP SCHEMA "content";

CREATE SCHEMA "content" AUTHORIZATION app;
-- "content".filmwork definition

-- Drop table

-- DROP TABLE "content".filmwork;

CREATE TABLE "content".filmwork (
	created timestamptz NOT NULL,
	modified timestamptz NOT NULL,
	id uuid NOT NULL,
	title varchar(255) NOT NULL,
	description text NULL,
	creation_date timestamptz NULL,
	rating float8 NULL,
	"type" text NULL,
	CONSTRAINT filmwork_pkey PRIMARY KEY (id)
);

-- Permissions

ALTER TABLE "content".filmwork OWNER TO app;
GRANT ALL ON TABLE "content".filmwork TO app;


-- "content".genre definition

-- Drop table

-- DROP TABLE "content".genre;

CREATE TABLE "content".genre (
	created timestamptz NOT NULL,
	modified timestamptz NOT NULL,
	id uuid NOT NULL,
	"name" varchar(255) NOT NULL,
	description text NULL,
	CONSTRAINT genre_pkey PRIMARY KEY (id)
);

-- Permissions

ALTER TABLE "content".genre OWNER TO app;
GRANT ALL ON TABLE "content".genre TO app;


-- "content".person definition

-- Drop table

-- DROP TABLE "content".person;

CREATE TABLE "content".person (
	created timestamptz NOT NULL,
	modified timestamptz NOT NULL,
	id uuid NOT NULL,
	full_name varchar(255) NOT NULL,
	CONSTRAINT person_pkey PRIMARY KEY (id)
);

-- Permissions

ALTER TABLE "content".person OWNER TO app;
GRANT ALL ON TABLE "content".person TO app;


-- "content".genre_filmwork definition

-- Drop table

-- DROP TABLE "content".genre_filmwork;

CREATE TABLE "content".genre_filmwork (
	id uuid NOT NULL,
	created timestamptz NOT NULL,
	filmwork_id uuid NOT NULL,
	genre_id uuid NOT NULL,
	CONSTRAINT genre_filmwork_pkey PRIMARY KEY (id),
	CONSTRAINT genre_filmwork_filmwork_id_9a46634f_fk_filmwork_id FOREIGN KEY (filmwork_id) REFERENCES "content".filmwork(id) DEFERRABLE INITIALLY DEFERRED,
	CONSTRAINT genre_filmwork_genre_id_d3bba77f_fk_genre_id FOREIGN KEY (genre_id) REFERENCES "content".genre(id) DEFERRABLE INITIALLY DEFERRED
);
CREATE INDEX genre_filmwork_filmwork_id_9a46634f ON content.genre_filmwork USING btree (filmwork_id);
CREATE INDEX genre_filmwork_genre_id_d3bba77f ON content.genre_filmwork USING btree (genre_id);

-- Permissions

ALTER TABLE "content".genre_filmwork OWNER TO app;
GRANT ALL ON TABLE "content".genre_filmwork TO app;


-- "content".person_filmwork definition

-- Drop table

-- DROP TABLE "content".person_filmwork;

CREATE TABLE "content".person_filmwork (
	id uuid NOT NULL,
	"role" text NULL,
	created timestamptz NOT NULL,
	filmwork_id uuid NOT NULL,
	person_id uuid NOT NULL,
	CONSTRAINT person_filmwork_pkey PRIMARY KEY (id),
	CONSTRAINT person_filmwork_filmwork_id_580ba752_fk_filmwork_id FOREIGN KEY (filmwork_id) REFERENCES "content".filmwork(id) DEFERRABLE INITIALLY DEFERRED,
	CONSTRAINT person_filmwork_person_id_c01da924_fk_person_id FOREIGN KEY (person_id) REFERENCES "content".person(id) DEFERRABLE INITIALLY DEFERRED
);
CREATE INDEX person_filmwork_filmwork_id_580ba752 ON content.person_filmwork USING btree (filmwork_id);
CREATE INDEX person_filmwork_person_id_c01da924 ON content.person_filmwork USING btree (person_id);

-- Permissions

ALTER TABLE "content".person_filmwork OWNER TO app;
GRANT ALL ON TABLE "content".person_filmwork TO app;


-- Permissions

GRANT ALL ON SCHEMA "content" TO app;


-- Extensions

CREATE extension IF NOT EXISTS "uuid-ossp";


-- Indexes

CREATE INDEX IF NOT exists filmwork_creation_date_idx ON content.filmwork(creation_date);
CREATE UNIQUE INDEX IF NOT exists filmwork_person_idx ON content.person_filmwork (filmwork_id, person_id, role);
CREATE UNIQUE INDEX IF NOT exists genre_filmwork_idx ON content.genre_filmwork (filmwork_id, genre_id);
