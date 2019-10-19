#!/usr/bin/env python3

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

import argparse, sys, os
from hikingmap.tracks import Tracks
from hikingmap.trackfinder import TrackFinder

def run_test(args, gpxfiles, scale = 50000, pagewidth = 20.0, pageheight = 28.7, \
             pageoverlap = 1.0, waypt_distance = 1, length_unit = "km", \
             page_order = "naturalorder"):
    dirname = os.path.abspath(gpxfiles[0] + ".result")
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    
    params = argparse.Namespace()
    params.scale = scale
    params.pagewidth = pagewidth
    params.pageheight = pageheight
    params.pageoverlap = pageoverlap 
    params.output_basename = os.path.join(dirname, "detail.")
    params.generate_overview = True
    params.waypt_distance = waypt_distance
    params.length_unit = length_unit
    params.page_order = page_order
    params.gpxfiles = gpxfiles
    params.debugmode = True
    params.verbose = True
    params.rendercommand = args.rendercommand
    params.renderoptions = args.renderoptions

    tracks = Tracks(params)
    trackfinder = TrackFinder(params, tracks)
    trackfinder.render()

# MAIN

parser = argparse.ArgumentParser()
parser.add_argument('rendercommand', nargs='?', default='hm-render-mapnik', \
                    help='render command')
parser.add_argument('renderoptions', nargs=argparse.REMAINDER, \
                    help='render options, rendercommand is required when adding options')
args = parser.parse_args()

run_test(args, gpxfiles = [ "test1.gpx" ])
run_test(args, gpxfiles = [ "test2.gpx" ])
run_test(args, gpxfiles = [ "test3.gpx" ])

