# Hikingmap testsuite

To improve quality a number of test tracks are included here, which produced or are still producing errors. Please refer to the issues on github for more information on the error of a specific test track.

## Usage

Run the script `runtest.py` with the desired renderer and its options as parameters. The script will try to calculate all pages for all test tracks, no error should be raised.

## Adding new test tracks

When you stumble upon a track which is not processed well by hikingmap, copy the track to this test directory and, to avoid copyright infringements, run `anongpx.py inputfile.gpx outputfile.gpx` to anonimize the data.
Next add the anonimized test file at the bottom of the `runtest.py` script and see if the error is reproducable. Once confirmed, please create a pull request for the new test track and report an issue on [the hikingmap github issues page](https://github.com/roelderickx/hikingmap/issues).

