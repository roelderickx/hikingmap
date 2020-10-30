# -*- coding: utf-8 -*-

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

import sys, os, tempfile, math
from lxml import etree
from .coordinate import Coordinate

class Tracks:
    def __init__(self):
        self.tracks = list()
        self.waypoints = list()
        self.tempwaypointfile = None


    def __del__(self):
        # remove temp file
        if self.tempwaypointfile is not None and os.path.isfile(self.tempwaypointfile):
            print("Removing temp file %s" % self.tempwaypointfile)
            os.remove(self.tempwaypointfile)


    # Read all tracks from a given list of gpx files and store them in memory
    def parse_files(self, gpxfiles):
        for gpxfile in gpxfiles:
            print("Reading file %s" % gpxfile)

            gpxdoc = etree.parse(gpxfile)
            gpxroot = gpxdoc.getroot()

            for gpxtrack in gpxroot.findall('trk', namespaces=gpxroot.nsmap):
                self.__parse_track(gpxtrack)


    def __parse_track(self, gpxtrack):
        namenode = gpxtrack.find('name', namespaces=gpxtrack.nsmap)
        trackname = namenode.text if namenode is not None and namenode.text else "[unnamed]"
        print("Found track %s" % trackname)

        track = list()
        for coord in gpxtrack.findall('trkseg/trkpt', namespaces=gpxtrack.nsmap):
            track.append(Coordinate(float(coord.get('lon')),
                                    float(coord.get('lat'))))

        # search if track connects to existing track in tracks
        foundindex = 0
        foundtrack = False
        for foundindex, existingtrack in enumerate(self.tracks):
            if existingtrack[0].equals(track[0]):
                print("=> same startpoint as track %d: reversing track" % foundindex)
                track.reverse()
            elif existingtrack[-1].equals(track[-1]):
                print("=> same endpoint as track %d: reversing track" % foundindex)
                track.reverse()

            if existingtrack[-1].equals(track[0]):
                print("=> connecting after track %d" % foundindex)
                newtrack = existingtrack + track[1:]
                self.tracks[foundindex] = newtrack
                foundtrack = True
                break
            elif existingtrack[0].equals(track[-1]):
                print("=> connecting before track %d" % foundindex)
                newtrack = track + existingtrack[1:]
                self.tracks[foundindex] = newtrack
                foundtrack = True
                break

        if not foundtrack:
            print("=> new track %d" % len(self.tracks))
            self.tracks.append(track)
    
    
    # Calculate waypoints after each waypt_distance for every track
    def calculate_waypoints(self, waypt_distance, length_unit):
        for (trackindex, track) in enumerate(self.tracks):
            print("Generating waypoints for track %d: %s - %s" % \
                        (trackindex, track[0].to_string(), track[-1].to_string()))
            
            track_waypoints = list()
            cumulDistance = 0
            prev_coord = track[0]
            for coord in track:
                cumulDistance = self.__add_waypoints(track_waypoints, prev_coord, coord, \
                                                     cumulDistance, waypt_distance, length_unit)
                prev_coord = coord

            print("Total track distance: %.2f %s" % (cumulDistance, length_unit))
            
            self.waypoints.append(track_waypoints)
    
    
    # calculate all waypoints between coord1 and coord2 and append them to track_waypoints
    # returns cumulative distance at coord2
    def __add_waypoints(self, track_waypoints, coord1, coord2, cumul_dist_at_coord1, \
                        waypt_distance, length_unit):
        if coord1.equals(coord2):
            if cumul_dist_at_coord1 == 0:
                track_waypoints.append((coord1, "0"))
            return cumul_dist_at_coord1
        else:
            cumul_dist_at_coord2 = \
                cumul_dist_at_coord1 + coord1.distance_haversine(coord2, length_unit)
            for dist in range(int(cumul_dist_at_coord1) + 1, int(cumul_dist_at_coord2) + 1):
                if dist % waypt_distance == 0:
                    d = dist - cumul_dist_at_coord1
                    waypt = coord1.calc_waypoint_on_line(coord2, d, length_unit)
                    track_waypoints.append((waypt, str(dist)))

            return cumul_dist_at_coord2


    # Write all waypoints to a temporary gpx file which will be deleted automatically in the destructor
    def write_waypoints_tempfile(self):
        xsischemaloc_qname = \
            etree.QName('http://www.w3.org/2001/XMLSchema-instance', 'schemaLocation')
        xsischemaloc_value = \
            'http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd'
        gpxattrs = { xsischemaloc_qname: xsischemaloc_value, \
                     'version': '1.0', \
                     'creator': 'hikingmap' }
        gpxnamespace = { None: 'http://www.topografix.com/GPX/1/0', \
                         'xsi': 'http://www.w3.org/2001/XMLSchema-instance' }
        gpxnode = etree.Element('gpx', gpxattrs, nsmap=gpxnamespace)
        
        for track_waypoints in self.waypoints:
            for (waypoint, description) in track_waypoints:
                gpxnode.append(waypoint.to_xml('wpt', description))

        gpxtree = etree.ElementTree(gpxnode)
        
        (fd, self.tempwaypointfile) = tempfile.mkstemp(prefix = "hikingmap_temp_waypoints", \
                                                       suffix = ".gpx")
        f = os.fdopen(fd, 'wb')
        gpxtree.write(f, encoding='utf-8', xml_declaration=True)
        f.close()

