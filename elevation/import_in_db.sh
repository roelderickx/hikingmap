#!/bin/bash

rm *.shp *.shx *.dbf *.index *.prj *.sql

for X in *.hgt
do
    gdal_contour -i 10 -snodata 32767 -a height ${X%%} ${X%%.hgt}c10.shp

    shapeindex ${X%%.hgt}c10.shp
    
    if [ ! -e elevation.sql ]; then
        shp2pgsql -p -s 4326 -I ${X%%.hgt}c10.shp elevation > elevation.sql
    fi
    shp2pgsql -a -D -s 4326 -i ${X%%.hgt}c10.shp elevation >> elevation.sql
done

psql -d gis -U gis -f elevation.sql

