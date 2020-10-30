# -*- coding: utf-8 -*-

# hikingmap -- render maps on paper using data from OpenStreetMap
# Copyright (C) 2015  Roel Derickx <roel.derickx AT gmail>

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

import argparse
from .tracks import Tracks
from .trackfinder import TrackFinder

def parse_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--scale', type=int, default=50000, \
                        help='scale denominator (default: %(default)s)')
    parser.add_argument('--pagewidth', type=float, default=20.0, \
                        help='paper width minus margin in cm (default: %(default)s)')
    parser.add_argument('--pageheight', type=float, default=28.7, \
                        help='paper height minus margin in cm (default: %(default)s)')
    parser.add_argument('--pageoverlap', type=float, default=1.0, \
                        help='page overlap in cm (default: %(default)s)')
    parser.add_argument('--overview', action='store_true', dest='generate_overview', \
                        help='generate overview map')
    parser.add_argument('-w', '--waypoints', type=int, default=1, dest='waypt_distance', \
                        help='add cumulative length each N km or mile, 0 to disable ' + \
                             '(default: %(default)s)')
    parser.add_argument('-u', '--unit', choices=[ 'km', 'mi' ], default='km', dest='length_unit', \
                        help='length unit in which the value of the waypoints parameter ' + \
                             'is expressed (default: %(default)s)')
    parser.add_argument('-o', '--page-order', choices=[ 'naturalorder', 'rectoverso', 'book' ], \
                        default='naturalorder', dest='page_order', \
                        help='order in which pages are generated (default: %(default)s)')
    parser.add_argument('-b', '--basename', default='detail.', dest='output_basename', \
                        help='output filename, hikingmap will add the pagenumber and extension ' + \
                             '(default: %(default)s)')
    parser.add_argument('--debug', action='store_true', dest='debugmode', \
                        help=argparse.SUPPRESS)
    parser.add_argument('-v', '--verbose', action='store_true', \
                        help='show verbose output')
    parser.add_argument('--gpx', required=True, nargs='+', dest='gpxfiles', \
                        help='one or more GPX tracks')
    parser.add_argument('rendercommand', nargs='?', default='hm-render-mapnik', \
                        help='render command, precede by -- when the previous parameter is --gpx')
    parser.add_argument('renderoptions', nargs=argparse.REMAINDER, \
                        help='render options, rendercommand is required when adding options')
    return parser.parse_args()


def main():
    params = parse_commandline()

    # read tracks
    tracks = Tracks()
    tracks.parse_files(params.gpxfiles)

    if params.waypt_distance > 0:
        tracks.calculate_waypoints(params.waypt_distance, params.length_unit)
        tracks.write_waypoints_tempfile()

    # calculate pages
    trackfinder = TrackFinder(params.scale, params.pagewidth, params.pageheight, params.pageoverlap, \
                              params.debugmode)
    trackfinder.calculate_pages(tracks)
    
    if params.generate_overview:
        trackfinder.add_overview_page()
    
    trackfinder.reorder_pages(params.page_order)
    
    # render
    trackfinder.render(params.rendercommand, params.renderoptions, params.output_basename, \
                       tracks.tempwaypointfile, params.gpxfiles, params.verbose)

