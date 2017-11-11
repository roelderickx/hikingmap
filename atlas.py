#!/usr/bin/env python2

# hikingmap -- render maps on paper using data from OpenStreetMap
# Copyright (C) 2015  Roel Derickx <roel.derickx AT gmail>
#                     Frederik Vincken <fvincken AT gmail>

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

import sys, os, math, getopt, tempfile, mapnik
from xml.dom import minidom
from collections import namedtuple

def enum(**enums):
    return type('Enum', (), enums)
Orientation = enum(Unknown = 0, Portrait = 1, Landscape = 2)

# global constants
earthRadius = 6371 # km
inch = 2.54 # cm


class Parameters:
    def __init__(self):
        # default parameters
        self.dpi = 200
        self.scale = 50000
        self.pagewidth = 20.0
        self.pageheight = 28.7
        self.pageoverlap = 1.0 # in cm
        self.mapstyle = "mapnik_style.xml"
        self.output_basename = "detail."
        self.output_format = "pdf"
        self.latitude = 0.0
        self.longitude = 0.0
        self.extrender = ""
        self.extrenderparams = ""
        self.verbose = False


    def __usage(self):
        print("Usage: " + sys.argv[0] + " [OPTION]... LAT LON\n"
              "Render map with coordinate LAT LON as the centerpoint\n\n"
              "  -d --dpi            Amount of detail to render " +
                                                "(default " + str(self.dpi) + ")\n"
              "  -s --scale          Scale denominator " +
                                                "(default " + str(self.scale) + ")\n"
              "     --pagewidth      Paper width minus margin in cm " +
                                                "(default " + str(self.pagewidth) + ")\n"
              "     --pageheight     Paper height minus margin in cm " +
                                                "(default " + str(self.pageheight) + ")\n"
              "     --pageoverlap    Page overlap in cm " +
                                                "(default " + str(self.pageoverlap) + ")\n"
              "  -m --mapstyle       Mapnik stylesheet file " +
                                                "(default " + self.mapstyle + ")\n"
              "  -b --basename       Output basename " +
                                                "(default " + self.output_basename + ")\n"
              "  -f --format         Output format, see mapnik documentation for\n"
              "                      possible values (default " + self.output_format + ")\n"
              "  -v --verbose        Display extra information while processing\n"
              "  -h --help           Display help and exit\n")


    # returns True if parameters could be parsed successfully
    def parse_commandline(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:s:m:b:f:vh", [
                "dpi=",
                "scale=",
                "pagewidth=",
                "pageheight=",
                "pageoverlap=",
                "mapstyle=",
                "basename=",
                "format=",
                "extrender=",
                "extrenderparams=",
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
            elif opt in ("-d", "--dpi"):
                self.dpi = int(arg)
            elif opt in ("-s", "--scale"):
                self.scale = int(arg)
            elif opt in ("--pagewidth"):
                self.pagewidth = float(arg)
            elif opt in ("--pageheight"):
                self.pageheight = float(arg)
            elif opt in ("--pageoverlap"):
                self.pageoverlap = float(arg)
            elif opt in ("-m", "--mapstyle"):
                self.mapstyle = str(arg)
            elif opt in ("-b", "--basename"):
                self.output_basename = str(arg)
            elif opt in ("-f", "--format"):
                self.output_format = str(arg)
            elif opt in ("--extrender"):
                self.extrender = str(arg)
            elif opt in ("--extrenderparams"):
                self.extrenderparams = str(arg)

        retval = True
        try:
            self.latitude = float(args[0])
            self.longitude = float(args[1])
        except:
            print("Nothing to do!")
            retval = False

        if self.verbose:
            print("Parameters:")
            print("dpi = " + str(self.dpi))
            print("scale = " + str(self.scale))
            print("pagewidth = " + str(self.pagewidth))
            print("pageheight = " + str(self.pageheight))
            print("pageoverlap = " + str(self.pageoverlap))
            print("mapstyle = " + self.mapstyle)
            print("output_basename = " + self.output_basename)
            print("output_format = " + self.output_format)
            print("latitude = " + str(self.latitude))
            print("longitude = " + str(self.longitude))

        return retval


class Coordinate:
    # lon and lat are coordinates, by default in degrees
    def __init__(self, lon, lat, isDegrees = True):
        if isDegrees:
            self.set_lon(lon)
            self.set_lat(lat)
        else:
            self.lon = math.degrees(lon)
            self.lat = math.degrees(lat)
            self.lon_radians = lon
            self.lat_radians = lat


    def __copy__(self, coord):
        self.set_lon(coord.lon)
        self.set_lat(coord.lat)


    def set_lon(self, lon):
        self.lon = lon
        self.lon_radians = math.radians(lon)


    def set_lat(self, lat):
        self.lat = lat
        self.lat_radians = math.radians(lat)


    def equals(self, coord):
        return self.lon == coord.lon and self.lat == coord.lat


    # calculate bearing between self and coord
    def bearing(self, coord):
        dLon = coord.lon_radians - self.lon_radians

        y = math.sin(dLon) * math.cos(coord.lat_radians)
        x = math.cos(self.lat_radians) * math.sin(coord.lat_radians) - \
            math.sin(self.lat_radians) * math.cos(coord.lat_radians) * math.cos(dLon)
        return math.atan2(y, x)


    # calculate distance in km between self and coord
    def distance_haversine(self, coord):
        dLat = coord.lat_radians - self.lat_radians
        dLon = coord.lon_radians - self.lon_radians

        a = math.sin(dLat/2) * math.sin(dLat/2) + \
            math.sin(dLon/2) * math.sin(dLon/2) * \
            math.cos(self.lat_radians) * math.cos(coord.lat_radians)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return earthRadius * c


    def to_string(self):
        return str(round(self.lon, 6)) + "," + str(round(self.lat, 6))


    # outputfile should be opened for writing
    def write_as_waypoint(self, outputfile, name):
        outputfile.write("<wpt lat=\"" + str(self.lat) + "\" lon=\"" + str(self.lon) + "\">\n")
        outputfile.write("    <name>" + name + "</name>\n")
        outputfile.write("</wpt>\n")


class Page(object):
    def __init__(self, parameters, min_coord, max_coord):
        self.minlon = min_coord.lon
        self.minlat = min_coord.lat
        self.maxlon = max_coord.lon
        self.maxlat = max_coord.lat


    def __copy__(self, page):
        self.minlon = page.minlon
        self.minlat = page.minlat
        self.maxlon = page.maxlon
        self.maxlat = page.maxlat


    def sizelon(self):
        return self.maxlon - self.minlon


    def sizelat(self):
        return self.maxlat - self.minlat


    def __std_render(self, parameters, filename):
        merc = mapnik.Projection('+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over')
        longlat = mapnik.Projection('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

        imgwidth = math.trunc(parameters.pagewidth / inch * parameters.dpi)
        imgheight = math.trunc(parameters.pageheight / inch * parameters.dpi)

        m = mapnik.Map(imgwidth, imgheight)
        mapnik.load_map(m, parameters.mapstyle)
        m.srs = merc.params()

        if hasattr(mapnik, 'Box2d'):
            bbox = mapnik.Box2d(self.minlon, self.minlat, self.maxlon, self.maxlat)
        else:
            bbox = mapnik.Envelope(self.minlon, self.minlat, self.maxlon, self.maxlat)

        transform = mapnik.ProjTransform(longlat, merc)
        merc_bbox = transform.forward(bbox)
        m.zoom_to_box(merc_bbox)

        #pdfprint = mapnik.printing.PDFPrinter(pagesize=[ (pagewidthcm+2) / 100, (pageheightcm+2) / 100], resolution=dpi)
        #pdfprint.render_map(m, filename)
        #context = pdfprint.get_context()
        #pdfprint.render_scale(m, ctx=context)
        #pdfprint.render_legend(m, ctx=context, attribution="(c) OpenStreetMap contributors")
        mapnik.render_to_file(m, filename, parameters.output_format)


    def render(self, parameters, filename):
        if not parameters.extrender:
            self.__std_render(parameters, filename)
        else:
            imgwidth = math.trunc(self.get_page_width() / inch * parameters.dpi)
            imgheight = math.trunc(self.get_page_height() / inch * parameters.dpi)
            
            cmd = parameters.extrender + " " + parameters.extrenderparams
            if parameters.verbose:
                cmd += " -v"
            cmd += " " + str(round(self.minlat, 6))
            cmd += " " + str(round(self.minlon, 6))
            cmd += " " + str(round(self.maxlat, 6))
            cmd += " " + str(round(self.maxlon, 6))
            cmd += " " + str(imgwidth)
            cmd += " " + str(imgheight)
            cmd += " " + filename
            os.system(cmd)


    def to_string(self, pagenumber):
        return "detail map " + str(pagenumber) + ": " + \
               Coordinate(self.minlon, self.minlat).to_string() + " - " + \
               Coordinate(self.maxlon, self.maxlat).to_string()


class Atlas:
    def __init__(self, parameters):
        self.pages = list()
        
        # center (lat,lon) on a page with given size
        pagesize_lon = self._convert_cm_to_degrees_lon(parameters.pagewidth, \
                                                       parameters.scale, parameters.latitude)
        pagesize_lat = self._convert_cm_to_degrees_lat(parameters.pageheight, parameters.scale)
        
        min_coord = Coordinate(parameters.longitude - pagesize_lon / 2, \
                               parameters.latitude - pagesize_lat / 2)
        max_coord = Coordinate(parameters.longitude + pagesize_lon / 2, \
                               parameters.latitude + pagesize_lat / 2)
        self.pages.append(Page(parameters, min_coord, max_coord))


    def _convert_cm_to_degrees_lon(self, lengthcm, scale, latitude):
        lengthkm = lengthcm / 100000.0 * scale
        return lengthkm / (111.11 * math.cos(math.radians(latitude)))


    def _convert_cm_to_degrees_lat(self, lengthcm, scale):
        lengthkm = lengthcm / 100000.0 * scale
        return lengthkm / 111.11



# MAIN

if not hasattr(mapnik, 'mapnik_version') and not mapnik.mapnik_version() >= 600:
    raise SystemExit('This script requires Mapnik >= 0.6.0)')

params = Parameters()
if not params.parse_commandline():
    sys.exit()

atlas = Atlas(params)

index = 1
for page in atlas.pages:
    print(page.to_string(index))
    page.render(params, \
                params.output_basename + \
                str(index).zfill(len(str(len(atlas.pages)))) + "." + \
                params.output_format)
    index += 1

