#!/bin/bash

rm *.tif *.sql

gdal_merge.py -v -o srtm.tif -ul_lr 2 52 7 49 *.hgt
gdal_translate -of GTiff -co "TILED=YES" -a_srs "+proj=latlong" srtm.tif srtm_adapted.tif
gdalwarp -of GTiff -co "TILED=YES" -srcnodata 32767 -t_srs "+proj=merc +ellps=sphere +R=6378137 +a=6378137 +units=m" -rcs -order 3 -tr 30 30 -multi srtm_adapted.tif srtm_warped.tif
gdaldem hillshade srtm_warped.tif srtm_hillshade.tif
#gdaldem color-relief srtm_warped.tif color-relief.def srtm_color_relief.tif -nearest_color_entry

raster2pgsql -t 50x50 -s 4326 -I srtm_hillshade.tif hillshade > hillshade.sql
psql -d gis -U gis -f hillshade.sql

