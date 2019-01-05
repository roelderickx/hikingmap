#!/usr/bin/env python

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
        self.track_area = Area(Coordinate(0.0, 0.0), Coordinate(0.0, 0.0))


    def __copy__(self, page):
        self.set_page_area(page)
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
    
    
    def set_page_area(self, area):
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


    def initialize_first_point(self, coord):
        self.track_area = Area(coord, coord) # size = 0
        self.set_orientation(self.orientation_unknown)


    def __track_area_outside_page(self):
        lon_outside = max(self.track_area.sizelon() - self.pagesizelon, 0)
        lat_outside = max(self.track_area.sizelat() - self.pagesizelat, 0)
        
        return lon_outside * self.track_area.sizelat() + \
               lat_outside * self.track_area.sizelon() - \
               lon_outside * lat_outside


    # recalculates page area needed to add new coordinate
    def add_next_point(self, prev_coord, coord):
        # add coord to track_area and recalculate page boundaries
        if coord.lon < self.track_area.minlon:
            self.track_area.minlon = coord.lon
            self.maxlon = self.track_area.maxlon
            self.minlon = self.maxlon - self.pagesizelon
        elif coord.lon > self.track_area.maxlon:
            self.track_area.maxlon = coord.lon
            self.minlon = self.track_area.minlon
            self.maxlon = self.minlon + self.pagesizelon

        if coord.lat < self.track_area.minlat:
            self.track_area.minlat = coord.lat
            self.maxlat = self.track_area.maxlat
            self.minlat = self.maxlat - self.pagesizelat
        elif coord.lat > self.track_area.maxlat:
            self.track_area.maxlat = coord.lat
            self.minlat = self.track_area.minlat
            self.maxlat = self.minlat + self.pagesizelat

        # does the track exceed the page boundary?
        outside_page = False
        if self.orientation == self.orientation_unknown:
            # try both portrait and landscape
            self.set_orientation(self.orientation_portrait)
            portrait_excess = self.__track_area_outside_page()
            self.set_orientation(self.orientation_landscape)
            landscape_excess = self.__track_area_outside_page()
            
            if portrait_excess == 0 and landscape_excess == 0:
                self.set_orientation(self.orientation_unknown)
            elif portrait_excess < landscape_excess:
                self.set_orientation(self.orientation_portrait)
                outside_page = (portrait_excess * landscape_excess > 0)
            elif portrait_excess > landscape_excess:
                self.set_orientation(self.orientation_landscape)
                outside_page = (portrait_excess * landscape_excess > 0)
        else:
            outside_page = (self.__track_area_outside_page() > 0)

        return outside_page


    def __calc_intersection_lon(self, l_start, l_end, lon):
        if l_start.lon == l_end.lon:
            return None
        else:
            return Coordinate(lon, \
                              (l_end.lat - l_start.lat) / (l_end.lon - l_start.lon) * \
                              (lon - l_start.lon) + l_start.lat)
    
    
    def __calc_intersection_lat(self, l_start, l_end, lat):
        if l_start.lat == l_end.lat:
            return None
        else:
            return Coordinate((lat - l_start.lat) * \
                              (l_end.lon - l_start.lon) / \
                              (l_end.lat - l_start.lat) + l_start.lon, \
                              lat)


    def calc_border_point(self, prev_coord, coord):
        '''
        # assert valid parameters and preconditions
        # prev_coord should be inside page area
        if not (self.minlon <= prev_coord.lon <= self.maxlon and \
                self.minlat <= prev_coord.lat <= self.maxlat):
            raise Exception("calc_border_point: prev_coord is not inside page area! " +
                        "report this bug to https://github.com/roelderickx/hikingmap/issues")
        # coord should be outside page area
        if self.minlon <= coord.lon <= self.maxlon and \
           self.minlat <= coord.lat <= self.maxlat:
            raise Exception("calc_border_point: coord is not outside page area! " +
                        "report this bug to https://github.com/roelderickx/hikingmap/issues")
        '''
        # calculate intersection point of line [prev_coord-coord]
        #                             and pagearea [minlon,minlat - maxlon,maxlat]
        intersect_coord = None
        if coord.lon <= self.minlon <= prev_coord.lon:
            intersect_coord = self.__calc_intersection_lon(coord, prev_coord, self.minlon)
        if intersect_coord == None and prev_coord.lon <= self.maxlon <= coord.lon:
            intersect_coord = self.__calc_intersection_lon(prev_coord, coord, self.maxlon)
        if intersect_coord == None and coord.lat <= self.minlat <= prev_coord.lat:
            intersect_coord = self.__calc_intersection_lat(coord, prev_coord, self.minlat)
        if intersect_coord == None and prev_coord.lat <= self.maxlat <= coord.lat:
            intersect_coord = self.__calc_intersection_lat(prev_coord, coord, self.maxlat)
        '''
        if intersect_coord == None:
            raise Exception("calc_border_point: no intersection found! " +
                        "report this bug to https://github.com/roelderickx/hikingmap/issues")
        '''
        return intersect_coord


    def add_page_to_overview(self, page):
        if page.pageindex == 1 or page.minlon < self.track_area.minlon:
            self.track_area.minlon = page.minlon
        if page.pageindex == 1 or page.maxlon > self.track_area.maxlon:
            self.track_area.maxlon = page.maxlon
        if page.pageindex == 1 or page.minlat < self.track_area.minlat:
            self.track_area.minlat = page.minlat
        if page.pageindex == 1 or page.maxlat > self.track_area.maxlat:
            self.track_area.maxlat = page.maxlat
        
        # recalculate orientation
        if self.track_area.maxlon - self.track_area.minlon < \
                        self.track_area.maxlat - self.track_area.minlat:
            self.set_orientation(self.orientation_portrait)
        else:
            self.set_orientation(self.orientation_landscape)
        
        # recalculate scale
        delta_lon = self.track_area.maxlon - self.track_area.minlon
        scale_lon = self._convert_degrees_lon_to_cm(delta_lon, self.track_area.minlat) \
                                   / (self.get_page_width() - self.pageoverlap)
        delta_lat = self.track_area.maxlat - self.track_area.minlat
        scale_lat = self._convert_degrees_lat_to_cm(delta_lat) \
                                   / (self.get_page_height() - self.pageoverlap)
        self.scale = max(scale_lon, scale_lat)


    def center_map(self):
        # set minlat to calculate pagesizelon correctly
        self.minlat = self.track_area.minlat
        
        # recalculate pagesizelon and pagesizelat
        self.set_orientation(self.orientation)

        # calculate page boundaries
        self.minlon = self.track_area.minlon + self.track_area.sizelon() / 2 - \
                        self.pagesizelon_full / 2
        self.maxlon = self.minlon + self.pagesizelon_full
        self.minlat = self.track_area.minlat + self.track_area.sizelat() / 2 - \
                        self.pagesizelat_full / 2
        self.maxlat = self.minlat + self.pagesizelat_full


    def render(self, parameters, tempgpxfile, filename):
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

    
    def to_string(self):
        mapname = "detail map " + str(self.pageindex)
        if self.pageindex == 0:
            mapname = "overview map"
        orientation_string = "portrait"
        if self.orientation == self.orientation_landscape:
            orientation_string = "landscape"
        retval = mapname + " (" + orientation_string + "): " + super(Page, self).to_string()
        if self.pageindex == 0:
            retval += ", scale = 1:" + str(round(self.scale))
        return retval

