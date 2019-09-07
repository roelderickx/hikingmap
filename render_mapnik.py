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
        self.dpi = 300
        self.basefilename = ""
        self.temptrackfile = ""
        self.tempwaypointfile = ""
        self.verbose = False
        self.mapstyle = "mapnik_style.xml"
        self.hikingmapstyle = "hikingmap_style.xml"
        self.output_format = "pdf"
        self.scale_factor = 1.0


    def __usage(self):
        print("Usage: " + sys.argv[0] + " [OPTION]... inputfile\n"
              "Render map page using mapnik / postrgesql toolchain\n\n"
              "  -o             Minimum longitude\n"
              "  -O             Maximum longitude\n"
              "  -a             Minimum latitude\n"
              "  -A             Maximum latitude\n"
              "  -w             Page width in cm\n"
              "  -h             Page height in cm\n"
              "  -d             DPI\n"
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
            elif opt in ("-d"):
                self.dpi = int(arg)
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


    def __get_xml_subtag_value(self, xmlnode, sublabelname, defaultvalue):
        elements = xmlnode.getElementsByTagName(sublabelname)
        return str(elements[0].firstChild.nodeValue) \
                      if elements and elements[0].childNodes \
                      else defaultvalue


    def parse_configfile(self):
        xmldoc = minidom.parse("render_mapnik.config.xml")
        xmlmapnik = xmldoc.getElementsByTagName('render_mapnik')[0]
        
        self.mapstyle = self.__get_xml_subtag_value(xmlmapnik, 'mapstyle', 'mapnik_style.xml')
        self.hikingmapstyle = self.__get_xml_subtag_value(xmlmapnik, 'hikingmapstyle', \
                                                          'hikingmap_style.xml')
        self.output_format = self.__get_xml_subtag_value(xmlmapnik, 'outputformat', 'pdf')
        self.scale_factor = float(self.__get_xml_subtag_value(xmlmapnik, 'scalefactor', '1.0'))
        
        xmlfontdirlist = xmlmapnik.getElementsByTagName('fontdirs')
        
        for xmlfontdir in xmlfontdirlist:
            fontdir = self.__get_xml_subtag_value(xmlfontdir, 'fontdir', '')
            if fontdir != '':
                mapnik.FontEngine.register_fonts(fontdir, True)
        
        return True



# MAIN

if not hasattr(mapnik, 'mapnik_version') or mapnik.mapnik_version() < 600:
    raise SystemExit('This script requires Mapnik >= 0.6.0)')

parameters = Parameters()
if not parameters.parse_commandline():
    sys.exit()

if not parameters.parse_configfile():
    sys.exit()

if not parameters.verbose:
    mapnik.logger.set_severity(getattr(mapnik.severity_type, 'None'))

merc = mapnik.Projection('+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over')
longlat = mapnik.Projection('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

imgwidth = math.trunc(parameters.pagewidth / inch * parameters.dpi)
imgheight = math.trunc(parameters.pageheight / inch * parameters.dpi)

m = mapnik.Map(imgwidth, imgheight)
mapnik.load_map(m, parameters.mapstyle)
mapnik.load_map(m, parameters.hikingmapstyle)
m.srs = merc.params()

if hasattr(mapnik, 'Box2d'):
    bbox = mapnik.Box2d(parameters.minlon, parameters.minlat, parameters.maxlon, parameters.maxlat)
else:
    bbox = mapnik.Envelope(parameters.minlon, parameters.minlat, parameters.maxlon, parameters.maxlat)

transform = mapnik.ProjTransform(longlat, merc)
merc_bbox = transform.forward(bbox)
m.zoom_to_box(merc_bbox)

for gpxfile in parameters.gpxfiles:
    gpxlayer = mapnik.Layer('GPXLayer')
    gpxlayer.datasource = mapnik.Ogr(file = gpxfile, layer = 'tracks')
    gpxlayer.styles.append('GPXStyle')
    m.layers.append(gpxlayer)

if parameters.temptrackfile != "":
    overviewlayer = mapnik.Layer('OverviewLayer')
    overviewlayer.datasource = mapnik.Ogr(file = parameters.temptrackfile, layer = 'tracks')
    overviewlayer.styles.append('GPXStyle')
    m.layers.append(overviewlayer)
elif parameters.tempwaypointfile != "":
    waypointlayer = mapnik.Layer('WaypointLayer')
    waypointlayer.datasource = mapnik.Ogr(file = parameters.tempwaypointfile, layer = 'waypoints')
    waypointlayer.styles.append('WaypointStyle')
    m.layers.append(waypointlayer)

#pdfprint = mapnik.printing.PDFPrinter(pagesize = [ 0.21, 0.297 ], \
#                                      margin = 0.005, resolution = parameters.dpi)
#context = pdfprint.get_cairo_context()
#pdfprint.render_scale(m, ctx=context)
#pdfprint.render_legend(m, ctx=context, attribution="(c) OpenStreetMap contributors")
#pdfprint.render_map(m, filename)

mapnik.render_to_file(m, parameters.basefilename + "." + parameters.output_format,
                      parameters.output_format,
                      parameters.scale_factor)

