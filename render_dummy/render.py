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

import sys, getopt, math, mapnik
from xml.dom import minidom

# global constants
inch = 2.54 # cm

class Parameters:
    def __init__(self):
        # default parameters
        self.minlon = 0.0
        self.maxlon = 0.0
        self.minlat = 0.0
        self.maxlat = 0.0
        self.pagewidth = 20.0
        self.pageheight = 28.7
        self.basefilename = ""
        self.temptrackfile = ""
        self.tempwaypointfile = ""
        self.verbose = False
        self.gpxfiles = [ ]


    def __usage(self):
        print("Usage: " + sys.argv[0] + " [OPTION]... gpxfiles\n"
              "Render map page using mapnik / postrgesql toolchain\n\n"
              "  -o             Minimum longitude\n"
              "  -O             Maximum longitude\n"
              "  -a             Minimum latitude\n"
              "  -A             Maximum latitude\n"
              "  -w             Page width in cm\n"
              "  -h             Page height in cm\n"
              "  -b             Filename, base without extension\n"
              "  -t             Temp track file to render\n"
              "  -y             Temp waypoints file to render\n"
              "  -v, --verbose  Verbose\n"
              "  --help         Display help and exit\n")


    # returns True if parameters could be parsed successfully
    def parse_commandline(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "o:O:a:A:w:h:d:b:t:y:v", [
                "verbose",
                "help"])
        except getopt.GetoptError:
            self.__usage()
            return False
        for opt, arg in opts:
            if opt == "--help":
                self.__usage()
                return False
            elif opt in ("-o"):
                self.minlon = float(arg)
            elif opt in ("-O"):
                self.maxlon = float(arg)
            elif opt in ("-a"):
                self.minlat = float(arg)
            elif opt in ("-A"):
                self.maxlat = float(arg)
            elif opt in ("-w"):
                self.pagewidth = float(arg)
            elif opt in ("-h"):
                self.pageheight = float(arg)
            elif opt in ("-b"):
                self.basefilename = arg
            elif opt in ("-t"):
                self.temptrackfile = arg
            elif opt in ("-y"):
                self.tempwaypointfile = arg
            elif opt in ("-v", "--verbose"):
                self.verbose = True
        
        self.gpxfiles = args

        if self.verbose:
            print("Parameters:")
            print("minlon = " + str(self.minlon))
            print("maxlon = " + str(self.maxlon))
            print("minlat = " + str(self.minlat))
            print("maxlat = " + str(self.maxlat))
            print("pagewidth = " + str(self.pagewidth))
            print("pageheight = " + str(self.pageheight))
            print("dpi = " + str(self.dpi))
            print("basefilename = " + self.basefilename)
            print("temptrackfile = " + self.temptrackfile)
            print("tempwaypointfile = " + self.tempwaypointfile)
            print("gpxfiles = " + ', '.join(self.gpxfiles))

        if not self.gpxfiles:
            print("Nothing to do!")
            return False
        else:
            return True



# MAIN
parameters = Parameters()
if not parameters.parse_commandline():
    sys.exit()
else:
    print("| Dummy rendering:")
    print("|   bbox (%.6f %.6f - %.6f %.6f)" % (parameters.minlon, parameters.minlat, \
                                                parameters.maxlon, parameters.maxlat))
    print("|   pagesize %.1fcm x %.1fcm" % (parameters.pagewidth, parameters.pageheight))
    print("|   filename %s.pdf" % parameters.basefilename)
    if parameters.temptrackfile:
        print("|   temptrackfile = %s" % parameters.temptrackfile)
    if parameters.tempwaypointfile:
        print("|   tempwaypointfile = %s" % parameters.tempwaypointfile)
    print("|   gpxfiles = %s" % ', '.join(parameters.gpxfiles))

