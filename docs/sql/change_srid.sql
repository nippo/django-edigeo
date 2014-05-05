update edigeo_parcelle set the_geom=ST_SetSRID(the_geom, 3857);
update edigeo_lieu_dit set the_geom=ST_SetSRID(the_geom, 3857);
update cad_prc set the_geom=ST_SetSRID(the_geom, 3857);
