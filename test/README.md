# Hikingmap testsuite

To improve quality a number of test tracks are included here, which produced or are still producing errors. Please refer to the issues on github for more information on the error of a specific test track.

## Usage

First copy the stylesheet and all necessary data, or at least create links to it.

```
ln -s ../openstreetmap-carto/data .
ln -s ../openstreetmap-carto/symbols/ .
ln -s ../openstreetmap-carto/mapnik_style.xml .
ln -s ../hikingmap_style.xml .
```

Next, run the script `runtest.py` without any parameter. The script will try to calculate all pages for all tracks, no error should be raised.

## Adding new test tracks

You may stumble upon a track which is not processed by hikingmap. When this happens, copy the track in this test directory and, to avoid copyright infringements, run `anongpx.py inputfile.gpx outputfile.gpx` to anonimize the data.
Next add the test at the bottom of to the `runtest.py` script and try if the error is reproducable by running `runtest.py` on the anonimized track.
If succesful, please create a pull request for the new test track and report an issue on [the hikingmap github issues page](https://github.com/roelderickx/hikingmap/issues).

