-- Table: edigeo_lieu_dit

-- DROP TABLE edigeo_lieu_dit;

CREATE TABLE edigeo_lieu_dit
(
  gid serial NOT NULL,
  gb_ident character varying(40),
  gb_idnum integer,
  tex10 character varying(80),
  tex2 character varying(80),
  tex3 character varying(80),
  tex4 character varying(80),
  tex5 character varying(80),
  tex6 character varying(80),
  tex7 character varying(80),
  tex8 character varying(80),
  tex9 character varying(80),
  tex character varying(80),
  the_geom geometry,
  CONSTRAINT edigeo_lieu_dit_pkey PRIMARY KEY (gid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE edigeo_lieu_dit
  OWNER TO nicolas;

-- Index: edigeo_lieu_dit_the_geom_gist

-- DROP INDEX edigeo_lieu_dit_the_geom_gist;

CREATE INDEX edigeo_lieu_dit_the_geom_gist
  ON edigeo_lieu_dit
  USING gist
  (the_geom);


