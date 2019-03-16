#!/usr/bin/env python

# runtest -- hikingmap integration test script
# Copyright (C) 2019  Roel Derickx <roel.derickx AT gmail>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys, os, mapnik

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from hikingmap_parameters import Parameters
from hikingmap_tracks import Tracks
from hikingmap_trackfinder import TrackFinder

def run_test(gpxfiles, dpi = 200, scale = 50000, scale_factor = 1.0, \
             pagewidth = 20.0, pageheight = 28.7, pageoverlap = 1.0, \
             waypt_distance = 1, length_unit = "km", page_order = "naturalorder"):
    dirname = gpxfiles[0] + ".result"
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    
    params = Parameters()
    params.dpi = dpi
    params.scale = scale
    params.scale_factor = scale_factor
    params.pagewidth = pagewidth
    params.pageheight = pageheight
    params.pageoverlap = pageoverlap # in cm
    #params.mapstyle = "mapnik_style.xml"
    #params.hikingmapstyle = "hikingmap_style.xml"
    params.output_basename = os.path.join(dirname, "detail.")
    params.output_format = "png"
    params.generate_overview = True
    params.waypt_distance = waypt_distance
    params.length_unit = length_unit
    params.page_order = page_order
    params.gpxfiles = gpxfiles
    params.debugmode = True
    params.verbose = True

    tracks = Tracks(params)
    trackfinder = TrackFinder(params, tracks)
    trackfinder.render()


# MAIN
if not hasattr(mapnik, 'mapnik_version') or mapnik.mapnik_version() < 600:
    raise SystemExit('This script requires Mapnik >= 0.6.0)')

# enable to search other paths for fonts
mapnik.FontEngine.register_fonts("/usr/share/fonts/noto", True)
mapnik.FontEngine.register_fonts("/usr/share/fonts/noto-cjk", True)
mapnik.FontEngine.register_fonts("/usr/share/fonts/TTF", True)

run_test(gpxfiles = [ "test1.gpx" ])
run_test(gpxfiles = [ "test2.gpx" ])
run_test(gpxfiles = [ "test3.gpx" ])

