# Hikingmap

A python script to render GPX track(s) on a minimum amount of pages. For installation instructions and additional requirements please visit [the hikingmap web page](https://roel.derickx.be/hikingmap/).

## Usage

Parameters:

| Parameter | Description
| --------- | -----------
| `-d, --dpi` | Amount of detail to render in dots per inch. This value is unrelated to the setting on your printer, a higher value will simply result in smaller icons, thinner roads and unreadable text
| `-s, --scale` | The scale denominator
| `-S, --scale-factor` | The scale factor to use when rendering to image formats
| `--pagewidth` | The width of the resulting map in portrait orientation. The application will automatically use pageheight when rendering in landscape orientation. The value should be the width of the desired papersize minus the horizontal margins on both sides.
| `--pageheight` | The height of the resulting map in portrait orientation. The application will automatically use pagewidth when rendering in landscape orientation. The value should be the height of the desired papersize minus the vertical margins on both sides.
| `--pageoverlap` | The amount of overlap between two consecutive pages, in cm.
| `-m, --mapstyle` | The filename of the mapnik stylesheet
| `--hikingmapstyle` | The filename of the hikingmap stylesheet. This stylesheet contains the styles to draw the GPX track and waypoints.
| `-w, --waypoints` | If this parameter is given the cumulative distance from the origin will be rendered each N kilometers.
| `-b, --basename` | Output filename base. All output file names will start with this parameter, followed by a sequence number and a file extension depending on the specified format.
| `-f, --format` | Output format. See the [mapnik documentation](http://mapnik.org/docs/v2.2.0/api/python/mapnik._mapnik-module.html#render_to_file) for possible values
| `-v, --verbose` | Display extra information while processing.
| `-h, --help` | Display help
| `gpxfiles` | The GPX track(s) to follow. More than one GPX file can be given, the script will render all tracks given.

The hikingmap script will try to render the complete track on a minimum of pages. Because it is particularly hard for an algorithm to decide what should be on the map and what shouldn't, the following rules are implemented:
* All tracks will be scanned and consecutive tracks will automatically be combined into a single track
* The tracks will be rendered in the given order. The script tries to center the track as much as possible and decides whether to use portrait or landscape to optimize paper usage
* If a track is finished and remaining tracks are to be rendered, only the parts which are not yet rendered will be processed. This might be only a part of the track, and only this part will be centered
