#!/bin/bash

GIS_DB=gis
GIS_USER=gis
TABLE_NAME=elevation
CREATE_TABLE=1 # modify to 0 if your table already exists and you just want to add data

rm *.shp *.shx *.dbf *.index *.prj *.sql

for X in *.hgt
do
    gdal_contour -i 10 -snodata 32767 -a height ${X%%} ${X%%.hgt}c10.shp

    shapeindex ${X%%.hgt}c10.shp
    
    if [ $CREATE_TABLE -eq 1 ]; then
        shp2pgsql -c -D -s 4326 -i ${X%%.hgt}c10.shp $TABLE_NAME >> elevation.sql
        CREATE_TABLE=2
    else
        shp2pgsql -a -D -s 4326 -i ${X%%.hgt}c10.shp $TABLE_NAME >> elevation.sql
    fi
    
    # disable analyze after each insert to improve performance
    sed -i -e 's/ANALYZE/--ANALYZE/g' elevation.sql
    # insert data
    psql -d $GIS_DB -U $GIS_USER -f elevation.sql
    
    rm *.shp *.shx *.dbf *.index *.prj *.sql
done

# analyze table
echo "ANALYZE \"$TABLE_NAME\"" | psql -d $GIS_DB -U $GIS_USER
# create the index we omitted in the beginning (shp2pgsql -c in stead of shp2pgsql -c -I)
if [ $CREATE_TABLE -eq 2 ]; then
    echo "CREATE INDEX ON \"$TABLE_NAME\" USING GIST (\"geom\");" | psql -d $GIS_DB -U $GIS_USER
fi

