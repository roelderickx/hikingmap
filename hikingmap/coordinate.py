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

import sys, math
from xml.dom import minidom

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


    def __get_earth_radius(self, length_unit):
        if length_unit == "mi":
            return 3959
        else: # default to km
            return 6371


    # calculate distance in km between self and coord
    def distance_haversine(self, coord, length_unit):
        dLat = coord.lat_radians - self.lat_radians
        dLon = coord.lon_radians - self.lon_radians

        a = math.sin(dLat/2) * math.sin(dLat/2) + \
            math.sin(dLon/2) * math.sin(dLon/2) * \
            math.cos(self.lat_radians) * math.cos(coord.lat_radians)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        return self.__get_earth_radius(length_unit) * c


    # returns the coordinate of the point which is on a given distance
    # from self in the direction of dest_coord
    def calc_waypoint_on_line(self, dest_coord, distance, length_unit):
        b = self.bearing(dest_coord)
        earth_radius = self.__get_earth_radius(length_unit)
        return Coordinate(#lon
                          self.lon_radians + \
                          math.atan2(math.sin(b) * \
                                     math.sin(distance/earth_radius) * \
                                     math.cos(self.lat_radians), \
                                     math.cos(distance/earth_radius) - \
                                     math.sin(self.lat_radians) * \
                                     math.sin(dest_coord.lat_radians)), \
                          #lat
                          math.asin(math.sin(self.lat_radians) * \
                                    math.cos(distance/earth_radius) + \
                                    math.cos(self.lat_radians) * \
                                    math.sin(distance/earth_radius) * \
                                    math.cos(b)),
                          False)


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

