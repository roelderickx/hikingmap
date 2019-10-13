#!/bin/bash

GIS_DB=gis
GIS_USER=gis
TABLE_NAME=elevation_ngi
CREATE_TABLE=1 # modify to 0 if your table already exists and you just want to add data

# merge ASCII files to GeoTIFF
gdal_merge.py -of GTIFF -o DTM20_BE_3812.tiff DTM20_??_ascii_L08.txt

# reproject merged file to Mercator projection
gdalwarp -s_srs EPSG:3812 -t_srs EPSG:4326 DTM20_BE_3812.tiff DTM20_BE_4326.tiff

# import in database
gdal_contour -i 10 -snodata 32767 -a height DTM20_BE_4326.tiff DTM20_BEc10.shp
shapeindex DTM20_BEc10.shp
if [ $CREATE_TABLE -eq 1 ]; then
    shp2pgsql -c -I -D -s 4326 -i DTM20_BEc10.shp $TABLE_NAME > elevation.sql
else
    shp2pgsql -a -D -s 4326 -i DTM20_BEc10.shp $TABLE_NAME > elevation.sql
fi
psql -d $GIS_DB -U $GIS_USER -f elevation.sql

rm *tiff *.shp *.shx *.dbf *.index *.prj *.sql

