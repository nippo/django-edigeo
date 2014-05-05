-- Table: edigeo_parcelle

-- DROP TABLE edigeo_parcelle;

CREATE TABLE edigeo_parcelle
(
  gid serial NOT NULL,
  gb_ident character varying(40),
  gb_idnum integer,
  coar character varying(1),
  codm character varying(80),
  idu character varying(20),
  indp character varying(80),
  supf numeric,
  tex2 character varying(80),
  tex character varying(80),
  the_geom geometry,
  insee_id integer,
  CONSTRAINT edigeo_parcelle_pkey PRIMARY KEY (gid),
  CONSTRAINT insee_id_refs_id_6a5128fb FOREIGN KEY (insee_id)
      REFERENCES insee (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED
)
WITH (
  OIDS=FALSE
);
ALTER TABLE edigeo_parcelle
  OWNER TO nicolas;

-- Index: edigeo_parcelle_the_geom_gist

-- DROP INDEX edigeo_parcelle_the_geom_gist;

CREATE INDEX edigeo_parcelle_the_geom_gist
  ON edigeo_parcelle
  USING gist
  (the_geom);
