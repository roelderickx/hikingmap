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

import sys, os, itertools, tempfile, mapnik
from xml.dom import minidom
from hikingmap_coordinate import Coordinate
from hikingmap_area import Area
from hikingmap_page import Page

class TrackFinder:
    def __init__(self, parameters, tracks):
        self.parameters = parameters
        self.tempwaypointfile = tracks.tempwaypointfile
        self.tempoverviewfile = ""
        self.pages = list()

        print("Calculating track order with minimum amount of pages")
        min_amount_pages = -1
        for trackpermutation in itertools.permutations(tracks.tracks):
            self.temppages = list()
            self.renderedareas = list()
            self.currentpageindex = 1
            self.currentpage = None #Page(parameters, self.currentpageindex)
            self.firstpointaccepted = False

            for track in trackpermutation:
                prev_coord = Coordinate(0.0, 0.0)
                for coord in track:
                    prev_coord = self.__add_point(prev_coord, coord)
                self.__flush()

            if min_amount_pages == -1 or len(self.temppages) < min_amount_pages:
                min_amount_pages = len(self.temppages)
                self.pages = self.temppages
                print("Found track permutation with %d pages" % min_amount_pages)

        if self.parameters.generate_overview:
            self.__add_page_overview()
        
        self.__reorder_pages()


    def __del__(self):
        # remove temp file
        if self.tempoverviewfile and os.path.isfile(self.tempoverviewfile):
            print("Removing temp file " + self.tempoverviewfile)
            os.remove(self.tempoverviewfile)


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
            self.temppages.append(self.currentpage)
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
            self.temppages.append(self.currentpage)
            self.renderedareas.append(self.currentpage.renderarea)
            self.__add_first_point(new_coord)
            self.__add_next_point(new_coord, coord)
        
        return new_coord


    def __add_page_overview(self):
        overviewdoc = minidom.Document()
        gpxnode = overviewdoc.createElement('gpx')
        gpxnode.setAttribute("version", "1.0")
        gpxnode.setAttribute("creator", "hikingmap")
        gpxnode.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        gpxnode.setAttribute("xmlns", "http://www.topografix.com/GPX/1/0")
        gpxnode.setAttribute("xsi:schemaLocation", \
              "http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd")
        
        minlon = -1
        minlat = -1
        maxlon = -1
        maxlat = -1
        for page in self.pages:
            tracknode = gpxnode.ownerDocument.createElement("trk")
            tracksegnode = gpxnode.ownerDocument.createElement("trkseg")
            for i in range(0, 5):
                if i in [0, 3, 4]:
                    lon = page.minlon
                else:
                    lon = page.maxlon
                if i in [0, 1, 4]:
                    lat = page.maxlat
                else:
                    lat = page.minlat
                trackptnode = gpxnode.ownerDocument.createElement("trkpt")
                trackptnode.setAttribute("lat", str(lat))
                trackptnode.setAttribute("lon", str(lon))
                tracksegnode.appendChild(trackptnode)
            tracknode.appendChild(tracksegnode)
            gpxnode.appendChild(tracknode)
            if minlon == -1 or page.minlon < minlon:
                minlon = page.minlon
            if maxlon == -1 or page.maxlon > maxlon:
                maxlon = page.maxlon
            if minlat == -1 or page.minlat < minlat:
                minlat = page.minlat
            if maxlat == -1 or page.maxlat > maxlat:
                maxlat = page.maxlat
        
        overviewdoc.appendChild(gpxnode)
        
        (fd, self.tempoverviewfile) = tempfile.mkstemp(prefix = "hikingmap_temp_overview", \
                                                       suffix = ".gpx")
        f = os.fdopen(fd, 'w')
        overviewdoc.writexml(f, "", "  ", "\n", "ISO-8859-1")
        f.close()
        
        overviewpage = Page(self.parameters, 0)
        overviewpage.set_area(Area(Coordinate(minlon, minlat), \
                                   Coordinate(maxlon, maxlat)))
        overviewpage.add_overlap_as_margin()
        
        if maxlon - minlon < maxlat - minlat:
            overviewpage.set_orientation(Page.orientation_portrait)
        else:
            overviewpage.set_orientation(Page.orientation_landscape)

        self.pages.insert(0, overviewpage)


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


    def render(self):
        for page in self.pages:
            if page != None:
                print(page.to_string())
                
                outfilename = \
                    self.parameters.output_basename + \
                    str(page.pageindex).zfill(len(str(len(self.pages)))) + "." + \
                    self.parameters.output_format

                if page.pageindex == 0:
                    page.render(self.parameters, self.tempoverviewfile, outfilename)
                else:
                    page.render(self.parameters, self.tempwaypointfile, outfilename)

