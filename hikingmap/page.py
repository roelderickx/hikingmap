#!/usr/bin/env python3

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

import sys, os, math, subprocess
from hikingmap.coordinate import Coordinate
from hikingmap.area import Area

class Page(Area):
    orientation_unknown = 0
    orientation_portrait = 1
    orientation_landscape = 2

    def __init__(self, parameters, pageindex):
        super(Page, self).__init__(Coordinate(0.0, 0.0), Coordinate(0.0, 0.0))
        self.pageindex = pageindex
        self.debugmode = parameters.debugmode
        self.scale = parameters.scale
        self.pagewidth = parameters.pagewidth
        self.pageheight = parameters.pageheight
        self.pageoverlap = parameters.pageoverlap
        self.set_orientation(self.orientation_unknown)
        self.track_area = Area(Coordinate(0.0, 0.0), Coordinate(0.0, 0.0))
        self.prev_track_area = Area(Coordinate(0.0, 0.0), Coordinate(0.0, 0.0))


    def __copy__(self, page):
        self.set_page_area(page)
        self.debugmode = page.debugmode
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
        self.prev_track_area = Area(coord, coord)
        self.set_orientation(self.orientation_unknown)


    # add coord to track_area and recalculate page boundaries
    def __add_point_to_track_area(self, coord):
        if coord.lon < self.track_area.minlon:
            self.prev_track_area.minlon = self.track_area.minlon #
            self.track_area.minlon = coord.lon
            self.maxlon = self.track_area.maxlon
            self.minlon = self.maxlon - self.pagesizelon
        elif coord.lon > self.track_area.maxlon:
            self.prev_track_area.maxlon = self.track_area.maxlon #
            self.track_area.maxlon = coord.lon
            self.minlon = self.track_area.minlon
            self.maxlon = self.minlon + self.pagesizelon

        if coord.lat < self.track_area.minlat:
            self.prev_track_area.minlat = self.track_area.minlat #
            self.track_area.minlat = coord.lat
            self.maxlat = self.track_area.maxlat
            self.minlat = self.maxlat - self.pagesizelat
        elif coord.lat > self.track_area.maxlat:
            self.prev_track_area.maxlat = self.track_area.maxlat #
            self.track_area.maxlat = coord.lat
            self.minlat = self.track_area.minlat
            self.maxlat = self.minlat + self.pagesizelat
    
    
    def __track_area_outside_page(self):
        lon_outside = max(self.track_area.sizelon() - self.pagesizelon, 0)
        lat_outside = max(self.track_area.sizelat() - self.pagesizelat, 0)
        
        return lon_outside * self.track_area.sizelat() + \
               lat_outside * self.track_area.sizelon() - \
               lon_outside * lat_outside


    # recalculates page area needed to add new coordinate
    def add_next_point(self, prev_coord, coord):
        self.__add_point_to_track_area(coord)

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


    def remove_last_point(self):
        self.track_area = self.prev_track_area
    
    
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


    def __raise_calc_border_error(self, message, prev_coord, coord):
        print("calc_border_point: %s" % message)
        print("  prev_coord = %s" % prev_coord.to_string())
        print("  coord = %s" % coord.to_string())
        print("  page area = %s" % self.to_string())
        raise Exception()


    def calc_border_point(self, prev_coord, coord):
        if self.debugmode:
            # assert valid parameters and preconditions
            # prev_coord should be inside page area
            if not (self.minlon <= prev_coord.lon <= self.maxlon and \
                    self.minlat <= prev_coord.lat <= self.maxlat):
                self.__raise_calc_border_error("prev_coord is not inside page area!", \
                                               prev_coord, coord)
            # coord should be outside page area
            if self.minlon <= coord.lon <= self.maxlon and \
               self.minlat <= coord.lat <= self.maxlat:
                self.__raise_calc_border_error("coord is not outside page area!", \
                                               prev_coord, coord)

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

        if self.debugmode:
            # assert valid result
            if intersect_coord == None:
                self.__raise_calc_border_error("no intersection found!", prev_coord, coord)
        
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


    def render(self, parameters, tempgpxfile, basefilename):
        args = [ parameters.rendercommand,
                 "--pagewidth", str(self.get_page_width()),
                 "--pageheight", str(self.get_page_height()),
                 "-b", basefilename ]
        if self.pageindex == 0 and parameters.generate_overview:
            args = args + [ "-t", tempgpxfile ]
        elif self.pageindex > 0 and parameters.waypt_distance > 0:
            args = args + [ "-y", tempgpxfile ]
        if parameters.verbose:
            args = args + [ "-v" ]
        if parameters.renderoptions:
            args = args + parameters.renderoptions
        args = args + [ os.path.abspath(f) for f in parameters.gpxfiles ]
        args = args + [ "bbox",
                        "-o", str(self.minlon), "-a", str(self.minlat),
                        "-O", str(self.maxlon), "-A", str(self.maxlat) ]
        
        retval = True
        try:
            process = subprocess.run(args, \
                                     stdout = subprocess.PIPE, \
                                     check = True, \
                                     universal_newlines = True)
            process.check_returncode()
            print(process.stdout, end = '')
        except subprocess.CalledProcessError as e:
            retval = False
        
        return retval

    
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

