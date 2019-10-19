#!/usr/bin/env python3

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
from xml.dom import minidom
from hikingmap.coordinate import Coordinate

class Tracks:
    def __init__(self, params):
        self.tempwaypointfile = ""
        self.tracks = list()
        self.__parse_files(params.gpxfiles)

        if params.waypt_distance > 0:
            self.__calculate_waypoints(params.waypt_distance, params.length_unit);


    def __del__(self):
        # remove temp file
        if self.tempwaypointfile and os.path.isfile(self.tempwaypointfile):
            print("Removing temp file " + self.tempwaypointfile)
            os.remove(self.tempwaypointfile)


    def __parse_files(self, gpxfiles):
        for gpxfile in gpxfiles:
            print("Reading file " + gpxfile)

            xmldoc = minidom.parse(gpxfile)
            xmltracklist = xmldoc.getElementsByTagName('trk')

            for xmltrack in xmltracklist:
                self.__parse_track(xmltrack)


    def __parse_track(self, xmltrack):
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
        foundtrack = False
        for foundindex, existingtrack in enumerate(self.tracks):
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
                newtrack = existingtrack + track[1:]
                self.tracks[foundindex] = newtrack
                foundtrack = True
                break
            elif existingtrack[0].equals(track[-1]):
                print("=> connecting before track " + str(foundindex))
                newtrack = track + existingtrack[1:]
                self.tracks[foundindex] = newtrack
                foundtrack = True
                break

        if not foundtrack:
            print("=> new track " + str(len(self.tracks)))
            self.tracks.append(track)


    # calculates all waypoints between coord1 and coord2
    # returns cumulative distance at coord2
    def __write_wpt(self, gpxnode, coord1, coord2, cumul_dist_at_coord1, \
                    waypt_distance, length_unit):
        if coord1.equals(coord2):
            if cumul_dist_at_coord1 == 0:
                coord1.append_to_xml_node(gpxnode, "0")
            return cumul_dist_at_coord1
        else:
            cumul_dist_at_coord2 = \
                cumul_dist_at_coord1 + coord1.distance_haversine(coord2, length_unit)
            for dist in range(int(cumul_dist_at_coord1) + 1, int(cumul_dist_at_coord2) + 1):
                if dist % waypt_distance == 0:
                    d = dist - cumul_dist_at_coord1
                    waypt = coord1.calc_waypoint_on_line(coord2, d, length_unit)
                    waypt.append_to_xml_node(gpxnode, str(dist))

            return cumul_dist_at_coord2


    def __generate_waypoints_track(self, gpxnode, track, waypt_distance, length_unit):
        cumulDistance = 0
        prev_coord = track[0]
        for coord in track:
            cumulDistance = self.__write_wpt(gpxnode, prev_coord, coord, \
                                             cumulDistance, waypt_distance, length_unit)
            prev_coord = coord

        print("Total track distance: %.2f %s" % (cumulDistance, length_unit))


    def __calculate_waypoints(self, waypt_distance, length_unit):
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
            self.__generate_waypoints_track(gpxnode, track, waypt_distance, length_unit)
            index += 1
        
        wayptdoc.appendChild(gpxnode)
        
        (fd, self.tempwaypointfile) = tempfile.mkstemp(prefix = "hikingmap_temp_waypoints", \
                                                       suffix = ".gpx")
        f = os.fdopen(fd, 'w')
        wayptdoc.writexml(f, "", "  ", "\n", "ISO-8859-1")
        f.close()

