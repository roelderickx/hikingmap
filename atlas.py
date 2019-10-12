#!/usr/bin/env python

# hikingmap -- render maps on paper using data from OpenStreetMap
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

import sys, getopt
from hikingmap_coordinate import Coordinate
from hikingmap_area import Area
from hikingmap_page import Page

class Parameters:
    def __init__(self):
        # default parameters
        self.scale = 50000
        self.pagewidth = 20.0
        self.pageheight = 28.7
        self.pageoverlap = 1.0 # in cm
        self.output_basename = "detail."
        self.render_dir = "render-mapnik"
        self.latitude = 0.0
        self.longitude = 0.0
        self.verbose = False
        # keep the hikingmap classes happy
        self.debugmode = False
        self.waypt_distance = 0
        self.gpxfiles = [ ]


    def __usage(self):
        print("Usage: " + sys.argv[0] + " [OPTION]... LAT LON\n"
              "Render map with coordinate LAT LON as the centerpoint\n\n"
              "  -s --scale          Scale denominator " +
                                                "(default " + str(self.scale) + ")\n"
              "     --pagewidth      Paper width minus margin in cm " +
                                                "(default " + str(self.pagewidth) + ")\n"
              "     --pageheight     Paper height minus margin in cm " +
                                                "(default " + str(self.pageheight) + ")\n"
              "     --pageoverlap    Page overlap in cm " +
                                                "(default " + str(self.pageoverlap) + ")\n"
              "  -b --basename       Output basename " +
                                                "(default " + self.output_basename + ")\n"
              "  -r --renderdir      Directory containing the renderscript render.py "
                                                "(default " + self.render_dir + ")\n"
              "  -v --verbose        Display extra information while processing\n"
              "  -h --help           Display help and exit\n")


    # returns True if parameters could be parsed successfully
    def parse_commandline(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "s:b:r:vh", [
                "scale=",
                "pagewidth=",
                "pageheight=",
                "pageoverlap=",
                "basename=",
                "renderdir=",
                "verbose",
                "help"])
        except getopt.GetoptError:
            self.__usage()
            return False
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                self.__usage()
                return False
            elif opt in ("-v", "--verbose"):
                self.verbose = True
            elif opt in ("-s", "--scale"):
                self.scale = int(arg)
            elif opt in ("--pagewidth"):
                self.pagewidth = float(arg)
            elif opt in ("--pageheight"):
                self.pageheight = float(arg)
            elif opt in ("--pageoverlap"):
                self.pageoverlap = float(arg)
            elif opt in ("-b", "--basename"):
                self.output_basename = str(arg)
            elif opt in ("-r", "--renderdir"):
                self.render_dir = str(arg)

        retval = True
        try:
            self.latitude = float(args[0])
            self.longitude = float(args[1])
        except:
            print("Nothing to do!")
            retval = False

        if self.verbose:
            print("Parameters:")
            print("scale = " + str(self.scale))
            print("pagewidth = " + str(self.pagewidth))
            print("pageheight = " + str(self.pageheight))
            print("pageoverlap = " + str(self.pageoverlap))
            print("output_basename = " + self.output_basename)
            print("render_dir = " + self.render_dir)
            print("latitude = " + str(self.latitude))
            print("longitude = " + str(self.longitude))

        return retval



class Atlas(Page):
    def __init__(self, parameters):
        super(Atlas, self).__init__(parameters, 1)
        
        # center (lat,lon) on a page with given size
        pagesize_lon = self._convert_cm_to_degrees_lon(parameters.pagewidth, \
                                                       parameters.scale, parameters.latitude)
        pagesize_lat = self._convert_cm_to_degrees_lat(parameters.pageheight, parameters.scale)
        
        min_coord = Coordinate(parameters.longitude - pagesize_lon / 2, \
                               parameters.latitude - pagesize_lat / 2)
        max_coord = Coordinate(parameters.longitude + pagesize_lon / 2, \
                               parameters.latitude + pagesize_lat / 2)
        
        self.set_page_area(Area(min_coord, max_coord))



# MAIN

params = Parameters()
if not params.parse_commandline():
    sys.exit()

atlas = Atlas(params)

print(atlas.to_string())
atlas.render(params, "", \
             params.output_basename + \
             str(atlas.pageindex))
#.zfill(len(str(len(atlas.pages)))) + "." + \

