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

import sys, os, math, mapnik
from hikingmap_coordinate import Coordinate
from hikingmap_area import Area

# global constants
inch = 2.54 # cm

class Page(Area):
    orientation_unknown = 0
    orientation_portrait = 1
    orientation_landscape = 2

    def __init__(self, parameters, pageindex):
        super(Page, self).__init__(Coordinate(0.0, 0.0), Coordinate(0.0, 0.0))
        self.pageindex = pageindex
        self.scale = parameters.scale
        self.pagewidth = parameters.pagewidth
        self.pageheight = parameters.pageheight
        self.pageoverlap = parameters.pageoverlap
        self.set_orientation(self.orientation_unknown)
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
        if self.orientation == self.orientation_landscape:
            return max(self.pagewidth, self.pageheight)
        else: # orientation_portrait or orientation_unknown:
            return min(self.pagewidth, self.pageheight)


    def get_page_height(self):
        if self.orientation == self.orientation_landscape:
            return min(self.pagewidth, self.pageheight)
        else: # orientation_portrait or orientation_unknown:
            return max(self.pagewidth, self.pageheight)


    def get_page_index(self):
        return self.pageindex
    
    
    def set_area(self, area):
        self.minlon = area.minlon
        self.minlat = area.minlat
        self.maxlon = area.maxlon
        self.maxlat = area.maxlat


    def add_overlap_as_margin(self):
        overlap_lon = \
            self._convert_cm_to_degrees_lon(self.get_page_width() - self.pageoverlap, \
                                            self.scale, self.minlat)
        self.minlon -= overlap_lon
        self.maxlon += overlap_lon

        overlap_lat = \
            self._convert_cm_to_degrees_lat(self.get_page_height() - self.pageoverlap, \
                                            self.scale)
        self.minlat -= overlap_lat
        self.maxlat += overlap_lat
    
    
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
        self.set_orientation(self.orientation_unknown)
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
        if self.orientation == self.orientation_unknown:
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
        if self.orientation == self.orientation_unknown and \
           self.sizelat() > self.minareasizelat:
            self.set_orientation(self.orientation_portrait)
        elif self.orientation == self.orientation_unknown and \
             self.sizelon() > self.minareasizelon:
            self.set_orientation(self.orientation_landscape)

        if self.orientation != self.orientation_unknown and outsidePage:
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


    def __std_render(self, parameters, tempgpxfile, filename):
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

        if self.pageindex == 0 and parameters.generate_overview:
            overviewlayer = mapnik.Layer('OverviewLayer')
            overviewlayer.datasource = mapnik.Ogr(file = tempgpxfile, layer = 'tracks')
            overviewlayer.styles.append('GPXStyle')
            m.layers.append(overviewlayer)
        elif self.pageindex > 0 and parameters.waypt_distance > 0:
            waypointlayer = mapnik.Layer('WaypointLayer')
            waypointlayer.datasource = mapnik.Ogr(file = tempgpxfile, layer = 'waypoints')
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
    
    
    def to_string(self):
        mapname = "detail map " + str(self.pageindex)
        if self.pageindex == 0:
            mapname = "overview map"
        orientation_string = "portrait"
        if self.orientation == self.orientation_landscape:
            orientation_string = "landscape"
        return mapname + " (" + orientation_string + "): " + super(Page, self).to_string()

