#!/usr/bin/env python

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

import sys, os, math, getopt, tempfile, mapnik #, mapnik.printing, itertools
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
        self.scale_factor = 1.0
        self.pagewidth = 20.0
        self.pageheight = 28.7
        self.pageoverlap = 1.0 # in cm
        self.mapstyle = "mapnik_style.xml"
        self.hikingmapstyle = "hikingmap_style.xml"
        self.output_basename = "detail."
        self.output_format = "pdf"
        self.waypt_distance = 1
        self.page_order = "naturalorder"
        self.gpxfiles = [ ]
        self.extrender = ""
        self.extrenderparams = ""
        self.verbose = False


    def __usage(self):
        print("Usage: " + sys.argv[0] + " [OPTION]... TRACK...\n"
              "Render maps based on given gpx TRACK(s)\n\n"
              "  -d --dpi            Amount of detail to render " +
                                                "(default " + str(self.dpi) + ")\n"
              "  -s --scale          Scale denominator " +
                                                "(default " + str(self.scale) + ")\n"
              "  -S --scale-factor   Scale factor " +
                                                "(default " + str(self.scale_factor) + ")\n"
              "     --pagewidth      Paper width minus margin in cm " +
                                                "(default " + str(self.pagewidth) + ")\n"
              "     --pageheight     Paper height minus margin in cm " +
                                                "(default " + str(self.pageheight) + ")\n"
              "     --pageoverlap    Page overlap in cm " +
                                                "(default " + str(self.pageoverlap) + ")\n"
              "  -m --mapstyle       Mapnik stylesheet file " +
                                                "(default " + self.mapstyle + ")\n"
              "     --hikingmapstyle Hikingmap stylesheet file " +
                                                "(default " + self.hikingmapstyle + ")\n"
              "  -w --waypoints      Add cumulative length each N km " +
                                                "(default " + str(self.waypt_distance) + ")\n"
              "  -o --page-order     Order in which pages are generated\n" +
              "                      [naturalorder, rectoverso, book] " +
                                                "(default " + str(self.page_order) + ")\n" +
              "  -b --basename       Output basename " +
                                                "(default " + self.output_basename + ")\n"
              "  -f --format         Output format, see mapnik documentation for\n"
              "                      possible values (default " + self.output_format + ")\n"
              "  -v --verbose        Display extra information while processing\n"
              "  -h --help           Display help and exit\n")


    # returns True if parameters could be parsed successfully
    def parse_commandline(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:s:S:m:w:o:b:f:vh", [
                "dpi=",
                "scale=",
                "scale-factor=",
                "pagewidth=",
                "pageheight=",
                "pageoverlap=",
                "mapstyle=",
                "hikingmapstyle=",
                "waypoints=",
                "page-order=",
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
            elif opt in ("-S", "--scale-factor"):
                self.scale_factor = float(arg)
            elif opt in ("--pagewidth"):
                self.pagewidth = float(arg)
            elif opt in ("--pageheight"):
                self.pageheight = float(arg)
            elif opt in ("--pageoverlap"):
                self.pageoverlap = float(arg)
            elif opt in ("-m", "--mapstyle"):
                self.mapstyle = str(arg)
            elif opt in ("--hikingmapstyle"):
                self.hikingmapstyle = str(arg)
            elif opt in ("-w", "--waypoints"):
                self.waypt_distance = int(arg)
            elif opt in ("-o", "--page-order"):
                self.page_order = str(arg)
            elif opt in ("-b", "--basename"):
                self.output_basename = str(arg)
            elif opt in ("-f", "--format"):
                self.output_format = str(arg)
            elif opt in ("--extrender"):
                self.extrender = str(arg)
            elif opt in ("--extrenderparams"):
                self.extrenderparams = str(arg)

        self.gpxfiles = args

        if self.verbose:
            print("Parameters:")
            print("dpi = " + str(self.dpi))
            print("scale = " + str(self.scale))
            print("scale factor = " + str(self.scale_factor))
            print("pagewidth = " + str(self.pagewidth))
            print("pageheight = " + str(self.pageheight))
            print("pageoverlap = " + str(self.pageoverlap))
            print("mapstyle = " + self.mapstyle)
            print("hikingmapstyle = " + self.hikingmapstyle)
            print("waypt_distance = " + str(self.waypt_distance))
            print("page_order = " + self.page_order)
            print("output_basename = " + self.output_basename)
            print("output_format = " + self.output_format)
            print("gpxfiles = " + ', '.join(self.gpxfiles))

        if not self.gpxfiles:
            print("Nothing to do!")
            return False
        else:
            return True


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


    def append_to_xml_node(self, gpxnode, name):
        wayptnode = gpxnode.ownerDocument.createElement("wpt")
        wayptnode.setAttribute("lat", str(self.lat))
        wayptnode.setAttribute("lon", str(self.lon))
        wayptnamenode = gpxnode.ownerDocument.createElement("name")
        wayptnametext = gpxnode.ownerDocument.createTextNode(name)
        wayptnamenode.appendChild(wayptnametext)
        wayptnode.appendChild(wayptnamenode)
        gpxnode.appendChild(wayptnode)


class Tracks:
    def __init__(self, gpxfiles):
        self.tempwaypointfile = ""
        self.tracks = list()

        for gpxfile in gpxfiles:
            print("Reading file " + gpxfile)

            xmldoc = minidom.parse(gpxfile)
            xmltracklist = xmldoc.getElementsByTagName('trk')

            for xmltrack in xmltracklist:
                elements = xmltrack.getElementsByTagName('name')
                trackname = str(elements[0].childNodes[0].nodeValue) \
                                      if elements and elements[0].childNodes \
                                      else "[unnamed]"
                print("Found track " + trackname)

                track = list()
                for coord in xmltrack.getElementsByTagName('trkpt'):
                    track.append(Coordinate(float(coord.attributes['lon'].value),
                                            float(coord.attributes['lat'].value)))

                # search if track connects to existing track in tracks
                foundindex = 0
                for existingtrack in self.tracks:
                    if existingtrack[0].equals(track[0]):
                        print("=> same startpoint as track " + str(foundindex) + \
                              ": reversing track")
                        track.reverse()
                    elif existingtrack[-1].equals(track[-1]):
                        print("=> same endpoint as track " + str(foundindex) + \
                              ": reversing track")
                        track.reverse()

                    if existingtrack[-1].equals(track[0]):
                        print("=> connecting after track " + str(foundindex))
                        newtrack = existingtrack + track
                        self.tracks[foundindex] = newtrack
                        break
                    elif existingtrack[0].equals(track[-1]):
                        print("=> connecting before track " + str(foundindex))
                        newtrack = track + existingtrack
                        self.tracks[foundindex] = newtrack
                        break
                    foundindex += 1

                if foundindex == len(self.tracks):
                    print("=> new track " + str(foundindex))
                    self.tracks.append(track)


    def __del__(self):
        # remove temp file
        if self.tempwaypointfile and os.path.isfile(self.tempwaypointfile):
            print("Removing temp file " + self.tempwaypointfile)
            os.remove(self.tempwaypointfile)


    # calculates all waypoints between coord1 and coord2
    # returns cumulative distance at coord2
    def __write_wpt(self, gpxnode, coord1, coord2, cumul_dist_at_coord1, waypt_distance):
        if coord1.equals(coord2):
            if cumul_dist_at_coord1 == 0:
                coord1.append_to_xml_node(gpxnode, "0")
            return cumul_dist_at_coord1
        else:
            b = coord1.bearing(coord2)
            cumul_dist_at_coord2 = cumul_dist_at_coord1 + coord1.distance_haversine(coord2)
            for km in range(int(cumul_dist_at_coord1) + 1, int(cumul_dist_at_coord2) + 1):
                if km % waypt_distance == 0:
                    d = km - cumul_dist_at_coord1
                    waypt = Coordinate(#lon
                                       coord1.lon_radians + \
                                       math.atan2(math.sin(b) * \
                                                  math.sin(d/earthRadius) * \
                                                  math.cos(coord1.lat_radians), \
                                                  math.cos(d/earthRadius) - \
                                                  math.sin(coord1.lat_radians) * \
                                                  math.sin(coord2.lat_radians)), \
                                       #lat
                                       math.asin(math.sin(coord1.lat_radians) * \
                                                 math.cos(d/earthRadius) + \
                                                 math.cos(coord1.lat_radians) * \
                                                 math.sin(d/earthRadius) * \
                                                 math.cos(b)),
                                       False)

                    waypt.append_to_xml_node(gpxnode, str(km))

            return cumul_dist_at_coord2


    def __generate_waypoints_track(self, gpxnode, track, waypt_distance):
        cumulDistance = 0
        prev_coord = Coordinate(track[0].lon, track[0].lat)
        for trackpoint in track[0:]:
            coord = Coordinate(trackpoint.lon, trackpoint.lat)
            cumulDistance = self.__write_wpt(gpxnode, prev_coord, coord, \
                                             cumulDistance, waypt_distance)
            prev_coord = coord

        print("Total track distance: " + str(round(cumulDistance, 2)) + " km")


    def calculate_waypoints(self, waypt_distance):
        wayptdoc = minidom.Document()
        gpxnode = wayptdoc.createElement('gpx')
        gpxnode.setAttribute("version", "1.0")
        gpxnode.setAttribute("creator", "hikingmap")
        gpxnode.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        gpxnode.setAttribute("xmlns", "http://www.topografix.com/GPX/1/0")
        gpxnode.setAttribute("xsi:schemaLocation", \
              "http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd")
        
        index = 0
        for track in self.tracks:
            print("Generating waypoints for track " + str(index) + ": " + \
                  track[0].to_string() + " - " + track[-1].to_string())
            self.__generate_waypoints_track(gpxnode, track, waypt_distance)
            index += 1
        
        wayptdoc.appendChild(gpxnode)
        
        (fd, self.tempwaypointfile) = tempfile.mkstemp(prefix = "hikingmap_temp_waypoints", \
                                                       suffix = ".gpx")
        f = os.fdopen(fd, 'w')
        wayptdoc.writexml(f, "", "  ", "\n", "ISO-8859-1")
        f.close()


class Area(object):
    def __init__(self, min_coord, max_coord):
        self.minlon = min_coord.lon
        self.minlat = min_coord.lat
        self.maxlon = max_coord.lon
        self.maxlat = max_coord.lat


    def __copy__(self, area):
        self.minlon = area.minlon
        self.minlat = area.minlat
        self.maxlon = area.maxlon
        self.maxlat = area.maxlat


    def _convert_cm_to_degrees_lon(self, lengthcm, scale, latitude):
        lengthkm = lengthcm / 100000.0 * scale
        return lengthkm / (111.11 * math.cos(math.radians(latitude)))


    def _convert_cm_to_degrees_lat(self, lengthcm, scale):
        lengthkm = lengthcm / 100000.0 * scale
        return lengthkm / 111.11


    def sizelon(self):
        return self.maxlon - self.minlon


    def sizelat(self):
        return self.maxlat - self.minlat


    def to_string(self):
        return Coordinate(self.minlon, self.minlat).to_string() + " - " + \
               Coordinate(self.maxlon, self.maxlat).to_string()


class Page(Area):
    def __init__(self, parameters, pageindex):
        super(Page, self).__init__(Coordinate(0.0, 0.0), Coordinate(0.0, 0.0))
        self.pageindex = pageindex
        self.scale = parameters.scale
        self.pagewidth = parameters.pagewidth
        self.pageheight = parameters.pageheight
        self.pageoverlap = parameters.pageoverlap
        self.set_orientation(Orientation.Unknown)
        self.minareasizelon = 0.0
        self.minareasizelat = 0.0
        self.renderarea = Area(Coordinate(0.0, 0.0), Coordinate(0.0, 0.0))


    def __copy__(self, page):
        self.set_area(page)
        self.scale = page.scale
        self.pagewidth = page.pagewidth
        self.pageheight = page.pageheight
        self.pageoverlap = page.pageoverlap
        self.set_orientation(page.orientation)


    def get_page_width(self):
        if self.orientation == Orientation.Landscape:
            return max(self.pagewidth, self.pageheight)
        else: # Orientation.Portrait or Orientation.Unknown:
            return min(self.pagewidth, self.pageheight)


    def get_page_height(self):
        if self.orientation == Orientation.Landscape:
            return min(self.pagewidth, self.pageheight)
        else: # Orientation.Portrait or Orientation.Unknown:
            return max(self.pagewidth, self.pageheight)


    def get_page_index(self):
        return self.pageindex
    
    
    def set_area(self, area):
        self.minlon = area.minlon
        self.minlat = area.minlat
        self.maxlon = area.maxlon
        self.maxlat = area.maxlat


    def set_orientation(self, orientation):
        self.orientation = orientation
        self.pagesizelon = \
            self._convert_cm_to_degrees_lon(self.get_page_width() - self.pageoverlap, \
                                            self.scale, self.minlat)
        self.pagesizelat = \
            self._convert_cm_to_degrees_lat(self.get_page_height() - self.pageoverlap, \
                                            self.scale)
        self.pagesizelon_full = \
            self._convert_cm_to_degrees_lon(self.get_page_width(), \
                                            self.scale, self.minlat)
        self.pagesizelat_full = \
            self._convert_cm_to_degrees_lat(self.get_page_height(), self.scale)


    # calculates the maximum square area on the page,
    def __calc_min_area(self):
        self.minareasizelon = \
            self._convert_cm_to_degrees_lon(min(self.pagewidth, self.pageheight) - \
                                            self.pageoverlap, self.scale, self.minlat)
        self.minareasizelat = \
            self._convert_cm_to_degrees_lat(min(self.pagewidth, self.pageheight) - \
                                            self.pageoverlap, self.scale)


    def initialize_first_point(self, coord):
        self.set_area(Area(coord, coord)) # size = 0
        self.set_orientation(Orientation.Unknown)
        self.__calc_min_area()


    # coord1 = previous point inside area
    # coord2 = next point outside area
    # returns coord2 if inside page,
    #                otherwise intersection between coord1-coord2 and page border
    def __get_intersection_page_border(self, coord1, coord2, pagearea):
        outsidePage = False
        coord3 = coord2

        # did we cross a vertical page border?
        if coord2.lon < pagearea.minlon < coord1.lon:
            outsidePage = True
            coord3 = Coordinate(pagearea.minlon, \
                                (coord2.lat - coord1.lat) / \
                                (coord2.lon - coord1.lon) * \
                                (pagearea.minlon - coord1.lon) + coord1.lat)
        elif coord1.lon < pagearea.maxlon < coord2.lon:
            outsidePage = True
            coord3 = Coordinate(pagearea.maxlon, \
                                (coord2.lat - coord1.lat) / \
                                (coord2.lon - coord1.lon) * \
                                (pagearea.maxlon - coord1.lon) + coord1.lat)

        # did we cross a horizontal page border?
        if coord3.lat < pagearea.minlat or coord3.lat > pagearea.maxlat:
            if coord2.lat < pagearea.minlat < coord1.lat:
                outsidePage = True
                coord3 = Coordinate((pagearea.minlat - coord1.lat) * \
                                    (coord2.lon - coord1.lon) / \
                                    (coord2.lat - coord1.lat) + coord1.lon,
                                    pagearea.minlat)
            elif coord1.lat < pagearea.maxlat < coord2.lat:
                outsidePage = True
                coord3 = Coordinate((pagearea.maxlat - coord1.lat) * \
                                    (coord2.lon - coord1.lon) / \
                                    (coord2.lat - coord1.lat) + coord1.lon,
                                    pagearea.maxlat)
        return outsidePage, coord3


    # recalculates page area needed to add new coordinate
    def add_next_point(self, prev_coord, coord):
        outsidePage = False
        new_coord = coord
        if self.orientation == Orientation.Unknown:
            # TODO try both portrait and landscape
            #      1. if both outsidePage == False -> continue
            #      2. prefer solution without outsidePage, adapt orientation etc
            #      3. if both outsidePage == True, prefer the solution with the greatest
            #         share, if equal -> portrait
            pass
        else:
            minpagelon = self.minlon
            minpagelat = self.minlat
            maxpagelon = self.maxlon
            maxpagelat = self.maxlat

            if coord.lon < self.minlon:
                minpagelon = maxpagelon - self.pagesizelon
            elif coord.lon > self.maxlon:
                maxpagelon = minpagelon + self.pagesizelon

            if coord.lat < self.minlat:
                minpagelat = maxpagelat - self.pagesizelat
            elif coord.lat > self.maxlat:
                maxpagelat = minpagelat + self.pagesizelat

            outsidePage, new_coord = \
                self.__get_intersection_page_border(prev_coord, coord, \
                                                    Area(Coordinate(minpagelon, minpagelat), \
                                                         Coordinate(maxpagelon, maxpagelat)))
        # adapt area to newlon, newlat
        if new_coord.lon < self.minlon:
            self.minlon = new_coord.lon
        elif new_coord.lon > self.maxlon:
            self.maxlon = new_coord.lon

        if new_coord.lat < self.minlat:
            self.minlat = new_coord.lat
        elif new_coord.lat > self.maxlat:
            self.maxlat = new_coord.lat

        # calculate page orientation and size
        if self.orientation == Orientation.Unknown and self.sizelat() > self.minareasizelat:
            self.set_orientation(Orientation.Portrait)
        elif self.orientation == Orientation.Unknown and self.sizelon() > self.minareasizelon:
            self.set_orientation(Orientation.Landscape)

        if self.orientation != Orientation.Unknown and outsidePage:
            self.center_map()
        else:
            outsidePage = False

        return outsidePage, new_coord


    def center_map(self):
        # calculate page boundaries
        minlon = self.minlon + self.sizelon() / 2 - self.pagesizelon_full / 2
        maxlon = minlon + self.pagesizelon_full
        minlat = self.minlat + self.sizelat() / 2 - self.pagesizelat_full / 2
        maxlat = minlat + self.pagesizelat_full

        self.renderarea = Area(Coordinate(minlon, minlat), Coordinate(maxlon, maxlat))
        self.set_area(self.renderarea)


    def __std_render(self, parameters, tempwaypointfile, filename):
        merc = mapnik.Projection('+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over')
        longlat = mapnik.Projection('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

        imgwidth = math.trunc(self.get_page_width() / inch * parameters.dpi)
        imgheight = math.trunc(self.get_page_height() / inch * parameters.dpi)

        m = mapnik.Map(imgwidth, imgheight)
        mapnik.load_map(m, parameters.mapstyle)
        mapnik.load_map(m, parameters.hikingmapstyle)
        m.srs = merc.params()

        if hasattr(mapnik, 'Box2d'):
            bbox = mapnik.Box2d(self.minlon, self.minlat, self.maxlon, self.maxlat)
        else:
            bbox = mapnik.Envelope(self.minlon, self.minlat, self.maxlon, self.maxlat)

        transform = mapnik.ProjTransform(longlat, merc)
        merc_bbox = transform.forward(bbox)
        m.zoom_to_box(merc_bbox)

        for gpxfile in parameters.gpxfiles:
            gpxlayer = mapnik.Layer('GPXLayer')
            gpxlayer.datasource = mapnik.Ogr(file = gpxfile, layer = 'tracks')
            gpxlayer.styles.append('GPXStyle')
            m.layers.append(gpxlayer)

        if parameters.waypt_distance > 0:
            waypointlayer = mapnik.Layer('WaypointLayer')
            waypointlayer.datasource = mapnik.Ogr(file = tempwaypointfile, layer = 'waypoints')
            waypointlayer.styles.append('WaypointStyle')
            m.layers.append(waypointlayer)

        #pdfprint = mapnik.printing.PDFPrinter(pagesize = [ 0.21, 0.297 ], \
        #                                      margin = 0.005, resolution = parameters.dpi)
        #context = pdfprint.get_cairo_context()
        #pdfprint.render_scale(m, ctx=context)
        #pdfprint.render_legend(m, ctx=context, attribution="(c) OpenStreetMap contributors")
        #pdfprint.render_map(m, filename)

        mapnik.render_to_file(m, filename,
                              parameters.output_format,
                              parameters.scale_factor)

    def render(self, parameters, tempwaypointfile, filename):
        if not parameters.extrender:
            self.__std_render(parameters, tempwaypointfile, filename)
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
            cmd += " " + " ".join(parameters.gpxfiles)
            os.system(cmd)
    
    
    def to_string(self, pagenumber):
        orientation_string = "portrait"
        if self.orientation == Orientation.Landscape:
            orientation_string = "landscape"
        return "detail map " + str(pagenumber) + " (" + orientation_string + "): " + \
               super(Page, self).to_string()


class TrackFinder:
    def __init__(self, parameters, tracks):
        self.parameters = parameters

        # TODO: code below works but some parts may not be rendered...
        '''
        self.minimumpages = list()
        print("Calculating track order with minimum amount of pages")
        minpages = -1
        for trackpermutation in itertools.permutations(tracks):
            self.pages = list()
            self.renderedareas = list()
            self.currentpageindex = 1
            self.currentpage = None #Page(parameters, self.currentpageindex)
            self.firstpointaccepted = False

            for track in trackpermutation:
                prev_coord = Coordinate(0.0, 0.0)
                for coord in track:
                    prev_coord = self.__add_point(prev_coord, coord)
                self.__flush()

            if minpages == -1 or len(self.pages) < minpages:
                minpages = len(self.pages)
                self.minimumpages = self.pages
                print("Found track permutation with %d pages" % minpages)
        '''
        self.pages = list()
        self.renderedareas = list()
        self.currentpageindex = 1
        self.currentpage = None #Page(parameters, self.currentpageindex)
        self.firstpointaccepted = False

        for track in tracks:
            prev_coord = Coordinate(0.0, 0.0)
            for coord in track:
                prev_coord = self.__add_point(prev_coord, coord)
            self.__flush()

        self.__reorder_pages()


    def __add_point(self, prev_coord, coord):
        if not self.__is_point_rendered(coord):
            if not self.firstpointaccepted:
                prev_coord = self.__add_first_point(coord)
            else:
                prev_coord = self.__add_next_point(prev_coord, coord)
        return prev_coord


    def __flush(self):
        if self.firstpointaccepted:
            self.currentpage.center_map()
            self.pages.append(self.currentpage)
            self.renderedareas.append(self.currentpage.renderarea)
            self.firstpointaccepted = False


    def __is_point_rendered(self, coord):
        return any(a.minlon <= coord.lon <= a.maxlon and \
                   a.minlat <= coord.lat <= a.maxlat for a in self.renderedareas)


    def __add_first_point(self, coord):
        self.currentpage = Page(self.parameters, self.currentpageindex)
        self.currentpage.initialize_first_point(coord)
        self.currentpageindex += 1
        self.firstpointaccepted = True
        return coord


    def __add_next_point(self, prev_coord, coord):
        ''' TODO:
        self.currentpage.add_next_point(coord)
        if self.currentpage.is_outside_page():
            new_coord = self.currentpage.get_border_intersection(prev_coord, coord)
            ...
        '''
        outsidePage, new_coord = self.currentpage.add_next_point(prev_coord, coord)
        
        if outsidePage:
            self.pages.append(self.currentpage)
            self.renderedareas.append(self.currentpage.renderarea)
            self.__add_first_point(new_coord)
            self.__add_next_point(new_coord, coord)
        
        return new_coord


    def __reorder_pages(self):
        if self.parameters.page_order == "rectoverso":
            oldindex = math.floor(len(self.pages) / 2)
            newindex = 1
            while (oldindex < len(self.pages)):
                self.pages.insert(newindex, self.pages.pop(oldindex))
                oldindex += 1
                newindex += 2
            
            print("Page order is rectoverso, new order =", end="")
            for page in self.pages:
                print(" " + str(page.get_page_index()), end="")
            print()
        elif self.parameters.page_order == "book":
            amount_empty_pages = (4 - (len(self.pages) % 4)) % 4
            for i in range(0, amount_empty_pages):
                self.pages.append(None)

            oldindex = len(self.pages) - 1
            newindex = 1
            while (newindex < oldindex):
                self.pages.insert(newindex, self.pages.pop(oldindex))
                newindex += 2
            
            # this page order requires recto-verso printing over the short edge of the
            # paper
            oldindex = 0
            newindex = 1
            while (oldindex < len(self.pages)):
                self.pages.insert(newindex, self.pages.pop(oldindex))
                oldindex += 4
                newindex += 4

            print("Page order is book, new order =", end="")
            for page in self.pages:
                if page != None:
                    print(" " + str(page.get_page_index()), end="")
                else:
                    print(" X", end="")
            print()
            print("WARNING: blank pages are not generated!")
        else:
            print("Page order is naturalorder")
            pass



# MAIN

if not hasattr(mapnik, 'mapnik_version') or mapnik.mapnik_version() < 600:
    raise SystemExit('This script requires Mapnik >= 0.6.0)')

# enable to search other paths for fonts
#mapnik.FontEngine.register_fonts("/usr/share/fonts/noto", True)
#mapnik.FontEngine.register_fonts("/usr/share/fonts/noto-cjk", True)
#mapnik.FontEngine.register_fonts("/usr/share/fonts/TTF", True)

params = Parameters()
if not params.parse_commandline():
    sys.exit()

tracks = Tracks(params.gpxfiles)
if params.waypt_distance > 0:
    tracks.calculate_waypoints(params.waypt_distance)

trackfinder = TrackFinder(params, tracks.tracks)

index = 1
for page in trackfinder.pages:
    if page != None:
        print(page.to_string(index))
        page.render(params, tracks.tempwaypointfile, \
                    params.output_basename + \
                    str(index).zfill(len(str(len(trackfinder.pages)))) + "." + \
                    params.output_format)
    index += 1

