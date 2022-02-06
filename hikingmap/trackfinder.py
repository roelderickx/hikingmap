# -*- coding: utf-8 -*-

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

import os
import math
import itertools
import tempfile
from lxml import etree
from .coordinate import Coordinate
from .page import Page

# global constants
MAX_TRACKS_PERM_CALC = 6

class TrackFinder:
    def __init__(self, scale, pagewidth, pageheight, pageoverlap, debugmode):
        self.scale = scale
        self.pagewidth = pagewidth
        self.pageheight = pageheight
        self.pageoverlap = pageoverlap
        self.debugmode = debugmode
        self.pages = list()
        self.tempoverviewfile = None

        self.__renderedareas = list()
        self.__currentpageindex = 1
        self.__currentpage = None
        self.__firstpointaccepted = False
        self.__pointskipped = True


    def __del__(self):
        # remove temp file
        if self.tempoverviewfile is not None and os.path.isfile(self.tempoverviewfile):
            print("Removing temp file %s" % self.tempoverviewfile)
            os.remove(self.tempoverviewfile)


    # Calculate the minimum amount of pages needed to render all tracks
    def calculate_pages(self, tracks):
        allpermutations = [ tracks.tracks ]

        if len(tracks.tracks) <= MAX_TRACKS_PERM_CALC:
            print("Calculating track order permutation resulting in a minimum amount of pages")
            print("This may take a while, checking %d track permutations" % \
                        math.factorial(len(tracks.tracks)))

            allpermutations = itertools.permutations(tracks.tracks)
        else:
            print("Too many tracks to calculate all track permutations")

        min_amount_pages = -1
        for permindex, trackpermutation in enumerate(allpermutations):
            self.__renderedareas = list()
            self.__currentpageindex = 1
            self.__currentpage = None
            self.__firstpointaccepted = False

            try:
                for track in trackpermutation:
                    self.__pointskipped = True
                    prev_coord = None
                    for coord in track:
                        self.__add_point(prev_coord, coord)
                        prev_coord = coord
                    self.__flush()
            except:
                if self.debugmode:
                    track_order = [ t[0].to_string() for t in trackpermutation ]
                    print("Error while calculating permutation %d, track order = %s" % \
                                (permindex, " // ".join(track_order)))
                    self.__debug_exception()
                raise

            if min_amount_pages == -1 or len(self.__renderedareas) < min_amount_pages:
                min_amount_pages = len(self.__renderedareas)
                self.pages = self.__renderedareas
                print("Found track permutation with %d pages" % min_amount_pages)


    def __add_point(self, prev_coord, coord):
        if not self.__is_point_rendered(coord):
            if not self.__firstpointaccepted:
                self.__add_first_point(coord)
            else:
                self.__add_next_point(prev_coord, coord)
            self.__pointskipped = False
        else:
            self.__pointskipped = True


    def __flush(self):
        if self.__firstpointaccepted:
            self.__currentpage.center_map()
            self.__renderedareas.append(self.__currentpage)
            self.__firstpointaccepted = False


    def __is_point_rendered(self, coord):
        return any(a.contains_coord(coord) for a in self.__renderedareas)


    def __add_first_point(self, coord):
        self.__currentpage = Page(self.__currentpageindex, \
                                  self.scale, self.pagewidth, self.pageheight, self.pageoverlap, \
                                  self.debugmode)
        self.__currentpage.initialize_first_point(coord)
        self.__currentpageindex += 1
        self.__firstpointaccepted = True


    def __get_closest_borderpoint(self, prev_coord, coord, include_currentpage = False):
        border_coords = [ page_prev_coord.calc_border_point(prev_coord, coord) \
                            for page_prev_coord in self.__renderedareas \
                                    if page_prev_coord.contains_coord(prev_coord) and \
                                       not page_prev_coord.contains_coord(coord) ]
        if include_currentpage:
            border_coords += [ self.__currentpage.calc_border_point(prev_coord, coord) ]

        border_coord = None
        for bc in border_coords:
            if not border_coord or \
               coord.distance_haversine(bc, 'km') < coord.distance_haversine(border_coord, 'km'):
                border_coord = bc

        return border_coord


    def __add_next_point(self, prev_coord, coord):
        outside_page = self.__currentpage.add_next_point(coord)

        if outside_page:
            self.__currentpage.remove_last_point()
            if not self.__pointskipped:
                border_coord = self.__get_closest_borderpoint(prev_coord, coord, True)
                self.__currentpage.add_next_point(border_coord)
            self.__currentpage.center_map()
            self.__renderedareas.append(self.__currentpage)
            if not self.__pointskipped:
                self.__add_first_point(border_coord)
                self.__add_next_point(border_coord, coord)
            else:
                if prev_coord:
                    border_coord = self.__get_closest_borderpoint(prev_coord, coord)
                    self.__add_first_point(border_coord)
                    self.__pointskipped = False
                    self.__add_next_point(border_coord, coord)
                else:
                    self.__add_first_point(coord)


    def __debug_exception(self):
        # output already calculated areas
        for area in self.__renderedareas:
            print(area.to_string())

        # render overview map for visualization
        self.pages = self.__renderedareas
        self.__add_overview_page('debug_overview.gpx')
        print("A debug overview map can be generated by running:")
        print(("[rendercommand] --pagewidth %.2f --pageheight %.2f -b debug_overview " + \
               "-t debug_overview.gpx -v [renderoptions] [gpxfiles] " + \
               "bbox -o %.15f -a %.15f -O %.15f -A %.15f") % \
              (self.pagewidth, self.pageheight, \
               self.pages[0].minlon, self.pages[0].minlat, \
               self.pages[0].maxlon, self.pages[0].maxlat))


    # Add an overview page on index 0 and write a temporary gpx file with the page layout
    # which will be deleted automatically in the destructor
    def add_overview_page(self):
        self.__add_overview_page()


    def __add_overview_page(self, filename=None):
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

        overviewpage = Page(0, self.scale, self.pagewidth, self.pageheight, self.pageoverlap, \
                            self.debugmode)

        for page in self.pages:
            overviewpage.add_page_to_overview(page)

            tracknode = etree.Element('trk')
            tracknamenode = etree.Element('name')
            tracknamenode.text = 'Page %d' % page.pageindex
            tracknode.append(tracknamenode)
            tracksegnode = etree.Element('trkseg')
            for i in range(0, 5):
                if i in [0, 3, 4]:
                    lon = page.minlon
                else:
                    lon = page.maxlon
                if i in [0, 1, 4]:
                    lat = page.maxlat
                else:
                    lat = page.minlat
                trackpoint = Coordinate(lon, lat)
                tracksegnode.append(trackpoint.to_xml('trkpt', None))
            tracknode.append(tracksegnode)
            gpxnode.append(tracknode)

        gpxtree = etree.ElementTree(gpxnode)

        fd = None
        if filename is None:
            (fd, self.tempoverviewfile) = tempfile.mkstemp(prefix = "hikingmap_temp_overview", \
                                                           suffix = ".gpx")
        else:
            fd = os.open(filename, os.O_RDWR | os.O_CREAT | os.O_TRUNC)

        f = os.fdopen(fd, 'wb')
        gpxtree.write(f, encoding='utf-8', xml_declaration=True)
        f.close()

        overviewpage.center_map()
        self.pages.insert(0, overviewpage)


    # Reorder the pages
    def reorder_pages(self, page_order):
        if page_order == "rectoverso":
            oldindex = math.floor(len(self.pages) / 2)
            newindex = 1
            while oldindex < len(self.pages):
                self.pages.insert(newindex, self.pages.pop(oldindex))
                oldindex += 1
                newindex += 2

            print("Page order is rectoverso, new order =", end="")
            for page in self.pages:
                print(" %d" % page.get_page_index(), end="")
            print()
        elif page_order == "book":
            amount_empty_pages = (4 - (len(self.pages) % 4)) % 4
            for i in range(0, amount_empty_pages):
                self.pages.append(None)

            oldindex = len(self.pages) - 1
            newindex = 1
            while newindex < oldindex:
                self.pages.insert(newindex, self.pages.pop(oldindex))
                newindex += 2

            # this page order requires recto-verso printing over the short edge of the
            # paper
            oldindex = 0
            newindex = 1
            while oldindex < len(self.pages):
                self.pages.insert(newindex, self.pages.pop(oldindex))
                oldindex += 4
                newindex += 4

            print("Page order is book, new order =", end="")
            for page in self.pages:
                if page is not None:
                    print(" %d" % page.get_page_index(), end="")
                else:
                    print(" X", end="")
            print()
            print("WARNING: blank pages are not generated!")
        else:
            print("Page order is naturalorder")


    def render(self, rendercommand, renderoptions, output_basename, tempwaypointfile, \
               gpxfiles, verbose):
        for (ordered_index, page) in enumerate(self.pages):
            if page is not None:
                print(page.to_string())

                outfilename = output_basename + str(ordered_index).zfill(len(str(len(self.pages))))

                if page.pageindex == 0:
                    page.render(rendercommand, renderoptions, outfilename, \
                                self.tempoverviewfile, gpxfiles, verbose)
                else:
                    page.render(rendercommand, renderoptions, outfilename, \
                                tempwaypointfile, gpxfiles, verbose)
