-- delete old data in favour of newer data
delete from planet_osm_line where osm_id in (select osm_id from new_line);
insert into planet_osm_line select * from new_line;
commit;

delete from planet_osm_nodes where id in (select id from new_nodes);
insert into planet_osm_nodes select * from new_nodes;
commit;

delete from planet_osm_point where osm_id in (select osm_id from new_point);
insert into planet_osm_point select * from new_point;
commit;

delete from planet_osm_polygon where osm_id in (select osm_id from new_polygon);
insert into planet_osm_polygon select * from new_polygon;
commit;

delete from planet_osm_rels where id in (select id from new_rels);
insert into planet_osm_rels select * from new_rels;
commit;

delete from planet_osm_roads where osm_id in (select osm_id from new_roads);
insert into planet_osm_roads select * from new_roads;
commit;

delete from planet_osm_ways where id in (select id from new_ways);
insert into planet_osm_ways select * from new_ways;
commit;

