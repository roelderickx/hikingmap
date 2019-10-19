#!/usr/bin/env python3

# anongpx -- anonimize GPX files to avoid copyright issues when filing bug reports
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

import argparse, os, random
from xml.dom import minidom

class Coordinate:
    def __init__(self, lon, lat):
        self.lon = lon
        self.lat = lat


class GpxTrack:
    def __init__(self, name):
        self.name = name
        self.track = list()


    def add_coord(self, lon, lat):
        self.track.append(Coordinate(lon, lat))
    
    
    def get_min_lon(self):
        return min([ coord.lon for coord in self.track ])
    
    
    def get_min_lat(self):
        return min([ coord.lat for coord in self.track ])


    def anonimize(self, lon_offset, lat_offset):
        for coord in self.track:
            coord.lon -= lon_offset
            coord.lat -= lat_offset


    def save_coords(self, gpxdoc, trksegnode):
        for coord in self.track:
            trkptnode = gpxdoc.createElement("trkpt")
            trkptnode.setAttribute("lat", str(coord.lat))
            trkptnode.setAttribute("lon", str(coord.lon))
            trksegnode.appendChild(trkptnode)


class GpxFile:
    def __init__(self, params):
        self.params = params
        self.tracks = list()
        
        xmldoc = minidom.parse(self.params.inputfile)
        xmltracklist = xmldoc.getElementsByTagName('trk')

        for xmltrack in xmltracklist:
            self.__parse_track(xmltrack)


    def __parse_track(self, xmltrack):
        elements = xmltrack.getElementsByTagName('name')
        trackname = str(elements[0].childNodes[0].nodeValue) \
                              if elements and elements[0].childNodes \
                              else "[unnamed]"
        if params.verbose:
            print("Found track %s" % trackname)

        track = GpxTrack(trackname)
        for coord in xmltrack.getElementsByTagName('trkpt'):
            track.add_coord(float(coord.attributes['lon'].value),
                            float(coord.attributes['lat'].value))
        if params.verbose:
            print("Added %d coordinates" % len(xmltrack.getElementsByTagName('trkpt')))

        self.tracks.append(track)


    def anonimize(self):
        lon_offset = min([ track.get_min_lon() for track in self.tracks ])
        lat_offset = random.random() * 10
           #min([ track.get_min_lat() for track in self.tracks ])
        
        for index, track in enumerate(self.tracks):
            track.name = ("track %03d" % index)
            track.anonimize(lon_offset, lat_offset)
    
    
    def save_file(self):
        gpxdoc = minidom.Document()
        gpxnode = gpxdoc.createElement('gpx')
        gpxnode.setAttribute("version", "1.0")
        gpxnode.setAttribute("creator", "anongpx")
        gpxnode.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        gpxnode.setAttribute("xmlns", "http://www.topografix.com/GPX/1/0")
        gpxnode.setAttribute("xsi:schemaLocation", \
              "http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd")

        for track in self.tracks:
            trknode = gpxdoc.createElement("trk")
            
            trknamenode = gpxdoc.createElement("name")
            trknametext = gpxdoc.createTextNode(track.name)
            trknamenode.appendChild(trknametext)
            
            trksegnode = gpxdoc.createElement("trkseg")
            track.save_coords(gpxdoc, trksegnode)
            
            trknode.appendChild(trknamenode)
            trknode.appendChild(trksegnode)
            gpxnode.appendChild(trknode)

        gpxdoc.appendChild(gpxnode)
        
        fd = os.open(self.params.outputfile, os.O_RDWR | os.O_CREAT)
        f = os.fdopen(fd, "w+")
        gpxdoc.writexml(f, "", "  ", "\n", "ISO-8859-1")
        f.close()


# MAIN

parser = argparse.ArgumentParser(description = "Anonimizes GPX file inputfile and writes " + \
                                               "the result to outputfile")
parser.add_argument('inputfile', help="Input GPX file")
parser.add_argument('outputfile', help="Anonimized output GPX file")
parser.add_argument('-v', dest = 'verbose', action = 'store_true')
params = parser.parse_args()

gpxfile = GpxFile(params)
gpxfile.anonimize()
gpxfile.save_file()

