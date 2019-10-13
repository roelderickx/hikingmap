# DTM of Belgium from NGI-IGN

The Belgian National Geographic Institute has released a DTM in a 20 meter resoluton for the area of Belgium. The files are available free of charge, however there are limitations on the use of the data. Visit the download page in [dutch](http://www.ngi.be/NL/NL1-5-5.shtm) or in [french](http://www.ngi.be/FR/FR1-5-5.shtm) and download the 3 DTM20 ASCII files for Brussels, Flanders and Wallonia in Lambert 2008 projection (which is EPSG:3812).

To import the data in the database you can use the script import\_belgium\_ngi\_in\_db.sh. It will merge the downloaded file to a GeoTIFF and reproject the Lambert 2008 coordinates to Mercator projection, before generating the contour lines and inserting them in the database.

Please note that each country has a different definition of sea level. The data may be more accurate than NASA's global 1-arc DEM but if both sources were imported respectively in- and outside Belgium the altitude lines would shift at belgium's borders.

