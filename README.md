# Hikingmap

A python script to calculate the minimum amount of pages needed to render one or more GPX tracks. The calculated pages will be passed to a render script of your choice. For installation instructions and additional requirements please consult the documentation folder or visit [the hikingmap web page](https://roel.derickx.be/hikingmap/).

## Usage

`hikingmap.py [OPTION]... TRACK...`

Options:

| Parameter | Description
| --------- | -----------
| `-s, --scale` | The scale denominator
| `--pagewidth` | The width of the resulting map in portrait orientation. The application will automatically use pageheight when rendering in landscape orientation. The value should be the width of the desired papersize minus the horizontal margins on both sides.
| `--pageheight` | The height of the resulting map in portrait orientation. The application will automatically use pagewidth when rendering in landscape orientation. The value should be the height of the desired papersize minus the vertical margins on both sides.
| `--pageoverlap` | The amount of overlap between two consecutive pages, in cm.
| `--overview` | Generate overview map
| `-w, --waypoints` | If this parameter is given the cumulative distance from the origin will be rendered each N kilometers or miles.
| `-u, --unit` | Length unit in which the value of the waypoints parameter is expressed. Possible values are km or mi (default km).
| `-o, --page-order` | Order in which pages are generated. Possible values are naturalorder, rectoverso or book (default naturalorder).
| `-b, --basename` | Output filename base. All output file names will start with this parameter, followed by a sequence number and a file extension depending on the specified format.
| `-r, --renderdir` | Directory containing the renderscript.
| `-v, --verbose` | Display extra information while processing.
| `-h, --help` | Display help
| `gpxfiles` | The GPX track(s) to follow. More than one GPX file can be given, the script will render all tracks given.

The hikingmap script will try to render the complete track on a minimum of pages. Because it is particularly hard for an algorithm to decide what should be on the map and what shouldn't, the following rules are implemented:
* All tracks will be scanned and consecutive tracks will automatically be combined into a single track
* The tracks will be rendered in the given order. The script tries to center the track as much as possible and decides whether to use portrait or landscape to optimize paper usage
* If a track is finished and remaining tracks are to be rendered, only the parts which are not yet rendered will be processed. This might be only a part of the track, and only this part will be centered

## Rendering

The actual rendering will be done by the render.py script found in the render directory (see the `-r` or `--renderdir` parameter).
By default the rendering will be done using mapnik by the renderscript in the render\_mapnik folder. This requires setting up a database and a stylesheet. Please consult the README.md file in the render\_mapnik folder as well as the documentation.

