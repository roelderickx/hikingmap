# Mapnik rendering

The render.py script renders an area with given boundaries using mapnik. It is designed to work with hikingmap but it can be used standalone as well if desired.

## Usage

`render.py [OPTION]... gpxfiles...`

Options:

| Parameter | Description
| --------- | -----------
| `-o` | Minimum longitude of the area boundaries
| `-O` | Maximum longitude of the area boundaries
| `-a` | Minimum latitude of the area boundaries
| `-A` | Maximum latitude of the area boundaries
| `-w` | Page width in cm
| `-h` | Page height in cm
| `-t` | Temp track file to render. This is used to draw the page boundaries of the overview map, hikingmap will save those as a temporary GPX file.
| `-y` | Temp waypoints file to render. This is used to render the distance each kilometer or mile, hikingmap will save those waypoints as a temporary GPX file.
| `-v, --verbose` | Display extra information while processing.
| `-h, --help` | Display help
| `gpxfiles` | The GPX track(s) to render.

## Configuration

Apart from these parameters there are some specific parameters for this renderer. They need to be configured in the file render_mapnik.config.xml. An example is included in this repository:

```
<?xml version="1.0" encoding="utf-8"?>
<render_mapnik>
    <mapstyle>mapnik_style.xml</mapstyle>
    <hikingmapstyle>hikingmap_style.xml</hikingmapstyle>
    <outputformat>pdf</outputformat>
    <dpi>300</dpi>
    <scalefactor>1.0</scalefactor>
    <fontdirs>
        <fontdir>/usr/share/fonts/noto</fontdir>
        <fontdir>/usr/share/fonts/noto-cjk</fontdir>
        <fontdir>/usr/share/fonts/TTF</fontdir>
    </fontdirs>
</render_mapnik>
```

Options:

| Tag | Description
| --- | -----------
| mapstyle | The filename of the mapnik stylesheet. This stylesheet contains the style to draw the actual map.
| hikingmapstyle | The filename of the hikingmap stylesheet. This stylesheet contains the styles to draw the GPX track and waypoints.
| outputformat | Output format. See the [mapnik documentation](http://mapnik.org/docs/v2.2.0/api/python/mapnik._mapnik-module.html#render_to_file) for possible values.
| dpi | Amount of detail to render in dots per inch. This value is unrelated to the setting on your printer, a higher value will simply result in smaller icons, thinner roads and unreadable text.
| scalefactor | The scale factor to use when rendering to image formats.
| fontdirs | Optional. Can contain one or more fontdir subtags with additional font directories to be used by mapnik.

