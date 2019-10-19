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

import sys, os, math
from hikingmap.coordinate import Coordinate

# global constants
earthCircumference = 40041.44 # km (average, equatorial 40075.017 km / meridional 40007.86 km)
cmToKmFactor = 100000.0

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
        lengthkm = lengthcm / cmToKmFactor * scale
        return lengthkm / ((earthCircumference / 360.0) * math.cos(math.radians(latitude)))


    def _convert_cm_to_degrees_lat(self, lengthcm, scale):
        lengthkm = lengthcm / cmToKmFactor * scale
        return lengthkm / (earthCircumference / 360.0)


    def _convert_degrees_lon_to_cm(self, delta_lon, latitude):
        return delta_lon * (earthCircumference / 360.0) * \
                       math.cos(math.radians(latitude)) * cmToKmFactor


    def _convert_degrees_lat_to_cm(self, delta_lat):
        return delta_lat * (earthCircumference / 360.0) * cmToKmFactor


    def sizelon(self):
        return self.maxlon - self.minlon


    def sizelat(self):
        return self.maxlat - self.minlat


    def to_string(self):
        return Coordinate(self.minlon, self.minlat).to_string() + " - " + \
               Coordinate(self.maxlon, self.maxlat).to_string()

