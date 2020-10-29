# Hikingmap

A python script to calculate the minimum amount of pages needed to render one or more GPX tracks. The calculated pages will be passed to a render script of your choice.

## Installation
Hikingmap depends only on lxml but you will also need to install a renderer to do something useful with it. See below under the [Rendering](#rendering) section.

### Using pip
```bash
pip install --upgrade hikingmap
```

### From source
Clone this repository and run the following command in the created directory.
```bash
python setup.py install
```

## Usage

`hikingmap [OPTION]... [rendercommand] [renderoptions]`

Options:

| Parameter | Description
| --------- | -----------
| `-s, --scale` | The scale denominator
| `--pagewidth` | The width of the resulting map in portrait orientation. The application will automatically use pageheight when rendering in landscape orientation. The value should be the width of the desired papersize minus the horizontal margins on both sides.
| `--pageheight` | The height of the resulting map in portrait orientation. The application will automatically use pagewidth when rendering in landscape orientation. The value should be the height of the desired papersize minus the vertical margins on both sides.
| `--pageoverlap` | The amount of overlap between two consecutive pages, in cm.
| `--overview` | Generate overview map
| `-w, --waypoints` | The cumulative distance from the origin will be rendered each N kilometers or miles. To disable this feature pass the value 0.
| `-u, --unit` | Length unit in which the value of the waypoints parameter is expressed. Possible values are km or mi (default km).
| `-o, --page-order` | Order in which pages are generated. Possible values are naturalorder, rectoverso or book (default naturalorder).
| `-b, --basename` | Output filename. Hikingmap will append the page number and the extension.
| `-v, --verbose` | Display extra information while processing.
| `-h, --help` | Display help
| `--gpx` | One or more GPX track(s) to follow. This is the only mandatory parameter.
| `rendercommand` | The render command, precede by -- when the previous parameter is --gpx
| `renderoptions` | Additional render options you want to pass, consult the documentation of the renderer. The rendercommand parameter is mandatory if you want to pass its options.

The hikingmap script will try to render the complete track on a minimum of pages. Because it is particularly hard for an algorithm to decide what should be on the map and what shouldn't, the following rules are implemented:
* All tracks will be scanned and consecutive tracks will automatically be combined into a single track
* The tracks will be rendered in the given order. The script tries to center the track as much as possible and decides whether to use portrait or landscape to optimize paper usage
* If a track is finished and remaining tracks are to be rendered, only the parts which are not yet rendered will be processed. This might be only a part of the track, and only this part will be centered

## Rendering

The actual rendering will be done by an external renderer (see the `rendercommand` and `renderoptions` parameters). Besides the dummy renderer included in this package, which only exists for debugging purposes or as a framework to write a new renderer, you have the choice between at least two renderers:

* [hm-render-mapnik](https://github.com/roelderickx/hm-render-mapnik): this is the default renderer used by hikingmap. All map data will be stored offline and elevation lines are supported, however the setup is rather difficult.

* [hm-render-landez](https://github.com/roelderickx/hm-render-landez): this is an alternative renderer which was initially written to be used with <a href="https://wiki.openstreetmap.org/wiki/MBTiles">MBTiles files</a>, but it can be configured to use a web based tile server as well. Please consult the documentation on the project page before use.

You may opt to write your own renderer. You can start by copying the dummy renderer, the parsing of the parameters is already in place as well as the ability to pass a center point and a scale. Hikingmap will pass the following parameters, you are free to use or ignore them as you wish:

| Parameter | Description
| --------- | -----------
| `--pagewidth` | The width of the page in cm
| `--pageheight` | The height of the page in cm
| `-b` | The output filename without extension, it is up to the renderer to add this
| `-t` | Temp track file to render, including the full path. This is used to draw the page boundaries of the overview map, hikingmap will save those as a temporary GPX file. This parameter is only passed when applicable.
| `-y` | Temp waypoints file to render, including the full path. This is used to render the distance each kilometer or mile, hikingmap will save those waypoints as a temporary GPX file. This parameter is only passed when applicable.
| `-v` | Verbose mode, hikingmap will pass this parameter when it is in verbose mode itself.
| `bbox` | This is the command to tell the renderer that the coordinates of the page boundaries will be passed in stead of the centerpoint and the scale
| `-o` | Minimum longitude of the page boundaries.
| `-a` | Minimum latitude of the page boundaries.
| `-O` | Maximum longitude of the page boundaries.
| `-A` | Minimum latitude of the page boundaries.

Of course you are free to add more parameters to the renderer which can be passed using the `renderoptions` parameter of hikingmap, or to provide long options for the existing parameters to facilitate using the renderer standalone.

## Results

Below you can find part of a rendered track. The maps were rendered on a 1:50000 scale for A4 paper size. It is included here only as an example to show how the track is rendered and how pages fit together.

![Example output](https://github.com/roelderickx/hikingmap/blob/master/example-output-thumb.png)

