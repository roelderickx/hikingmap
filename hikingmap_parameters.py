#!/usr/bin/env python

# hikingmap -- render maps on paper using data from OpenStreetMap
# Copyright (C) 2015  Frederik Vincken <fvincken AT gmail>

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

class Parameters:
    def __init__(self):
        # default parameters
        self.scale = 50000
        self.pagewidth = 20.0
        self.pageheight = 28.7
        self.pageoverlap = 1.0 # in cm
        self.output_basename = "detail."
        self.generate_overview = False
        self.waypt_distance = 1
        self.length_unit = "km"
        self.page_order = "naturalorder"
        self.render_dir = "render_mapnik"
        self.gpxfiles = [ ]
        self.debugmode = False
        self.verbose = False


    def __usage(self):
        print("Usage: " + sys.argv[0] + " [OPTION]... TRACK...\n"
              "Render maps based on given gpx TRACK(s)\n\n"
              "  -s --scale          Scale denominator "
                                                "(default " + str(self.scale) + ")\n"
              "     --pagewidth      Paper width minus margin in cm "
                                                "(default " + str(self.pagewidth) + ")\n"
              "     --pageheight     Paper height minus margin in cm "
                                                "(default " + str(self.pageheight) + ")\n"
              "     --pageoverlap    Page overlap in cm "
                                                "(default " + str(self.pageoverlap) + ")\n"
              "     --overview       Generate overview map\n"
              "  -w --waypoints      Add cumulative length each N km or mile "
                                                "(default " + str(self.waypt_distance) + ")\n"
              "  -u --unit           Length unit in which the value of the waypoints\n"
              "                      parameter is expressed [km, mi] "
                                                "(default " + str(self.length_unit) + ")\n"
              "  -o --page-order     Order in which pages are generated\n"
              "                      [naturalorder, rectoverso, book] "
                                                "(default " + str(self.page_order) + ")\n"
              "  -b --basename       Output basename "
                                                "(default " + self.output_basename + ")\n"
              "  -r --renderdir      Directory containing the renderscript render.py "
                                                "(default " + self.render_dir + ")\n"
              "  -v --verbose        Display extra information while processing\n"
              "  -h --help           Display help and exit\n")


    # returns True if parameters could be parsed successfully
    def parse_commandline(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:s:w:u:o:b:r:vh", [
                "scale=",
                "pagewidth=",
                "pageheight=",
                "pageoverlap=",
                "overview",
                "waypoints=",
                "unit=",
                "page-order=",
                "basename=",
                "renderdir=",
                "debug",
                "verbose",
                "help"])
        except getopt.GetoptError:
            self.__usage()
            return False
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                self.__usage()
                return False
            elif opt in ("--debug"):
                self.debugmode = True
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
            elif opt in ("--overview"):
                self.generate_overview = True
            elif opt in ("-w", "--waypoints"):
                self.waypt_distance = int(arg)
            elif opt in ("-u", "--unit"):
                if arg == "mi":
                    self.length_unit = arg
                else: # default km
                    self.length_unit = "km"
            elif opt in ("-o", "--page-order"):
                self.page_order = str(arg)
            elif opt in ("-b", "--basename"):
                self.output_basename = str(arg)
            elif opt in ("-r", "--renderdir"):
                self.render_dir = str(arg)

        self.gpxfiles = args

        if self.verbose:
            print("Parameters:")
            print("scale = " + str(self.scale))
            print("pagewidth = " + str(self.pagewidth))
            print("pageheight = " + str(self.pageheight))
            print("pageoverlap = " + str(self.pageoverlap))
            print("overview = " + str(self.generate_overview))
            print("waypt_distance = " + str(self.waypt_distance))
            print("length_unit = " + self.length_unit)
            print("page_order = " + self.page_order)
            print("output_basename = " + self.output_basename)
            print("render_dir = " + self.render_dir)
            print("gpxfiles = " + ', '.join(self.gpxfiles))

        if not self.gpxfiles:
            print("Nothing to do!")
            return False
        else:
            return True

