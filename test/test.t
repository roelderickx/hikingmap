  $ [ "$0" != "/bin/bash" ] || shopt -s expand_aliases
  $ [ -n "$PYTHON" ] || PYTHON="`which python`"
  $ alias hikingmap="TMPDIR=$TESTDIR PYTHONPATH=$TESTDIR/.. $PYTHON -m hikingmap"

usage:
  $ hikingmap -h
  usage: __main__.py [-h] [-s SCALE] [--pagewidth PAGEWIDTH]
                     [--pageheight PAGEHEIGHT] [--pageoverlap PAGEOVERLAP]
                     [--overview] [-w WAYPT_DISTANCE] [-u {km,mi}]
                     [-o {naturalorder,rectoverso,book}] [-b OUTPUT_BASENAME]
                     [-v] --gpx GPXFILES [GPXFILES ...]
                     [rendercommand] ...
  
  positional arguments:
    rendercommand         render command, precede by -- when the previous
                          parameter is --gpx
    renderoptions         render options, rendercommand is required when adding
                          options
  
  optional arguments:
    -h, --help            show this help message and exit
    -s SCALE, --scale SCALE
                          scale denominator (default: 50000)
    --pagewidth PAGEWIDTH
                          paper width minus margin in cm (default: 20.0)
    --pageheight PAGEHEIGHT
                          paper height minus margin in cm (default: 28.7)
    --pageoverlap PAGEOVERLAP
                          page overlap in cm (default: 1.0)
    --overview            generate overview map
    -w WAYPT_DISTANCE, --waypoints WAYPT_DISTANCE
                          add cumulative length each N km or mile, 0 to disable
                          (default: 1)
    -u {km,mi}, --unit {km,mi}
                          length unit in which the value of the waypoints
                          parameter is expressed (default: km)
    -o {naturalorder,rectoverso,book}, --page-order {naturalorder,rectoverso,book}
                          order in which pages are generated (default:
                          naturalorder)
    -b OUTPUT_BASENAME, --basename OUTPUT_BASENAME
                          output filename, hikingmap will add the pagenumber and
                          extension (default: detail.)
    -v, --verbose         show verbose output
    --gpx GPXFILES [GPXFILES ...]
                          one or more GPX tracks

nooverview:
  $ hikingmap --debug -v -s 50000 --pagewidth 20.0 --pageheight 28.7 --pageoverlap 1.0 -w 1 -u km -o naturalorder -b $TESTDIR/detail. --gpx $TESTDIR/test3.gpx -- $TESTDIR/render-test.py
  Reading file /home/roel/hiking/hikingmap/test/test3.gpx
  Found track track 000
  => new track 0
  Found track track 001
  => new track 1
  Found track track 002
  => new track 2
  Found track track 003
  => new track 3
  Generating waypoints for track 0: 0.115582,36.429966 - 0.113308,36.426573
  Total track distance: 0.47 km
  Generating waypoints for track 1: 0.033205,36.488041 - 0.031212,36.487269
  Total track distance: 0.20 km
  Generating waypoints for track 2: 0.261325,36.34589 - 0.264876,36.342772
  Total track distance: 0.48 km
  Generating waypoints for track 3: 0.308385,36.244406 - 0.001886,36.594681
  Total track distance: 107.84 km
  Calculating track order permutation resulting in a minimum amount of pages
  This may take a while, checking 24 track permutations
  Found track permutation with 6 pages
  Found track permutation with 5 pages
  Found track permutation with 4 pages
  Page order is naturalorder
  detail map 1 (portrait): 0.201255,36.242158 - 0.312732,36.371175
  | Test rendering:
  |   bbox (0.201255 36.242158 - 0.312732 36.371175)
  |   pagesize 20.0cm x 28.7cm
  |   filename /home/roel/hiking/hikingmap/test/detail.0.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test3.gpx
  detail map 2 (landscape): 0.109946,36.355882 - 0.270172,36.445788
  | Test rendering:
  |   bbox (0.109946 36.355882 - 0.270172 36.445788)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.1.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test3.gpx
  detail map 3 (landscape): -0.023655,36.426579 - 0.136694,36.516486
  | Test rendering:
  |   bbox (-0.023655 36.426579 - 0.136694 36.516486)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.2.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test3.gpx
  detail map 4 (portrait): -0.031275,36.489921 - 0.080589,36.618937
  | Test rendering:
  |   bbox (-0.031275 36.489921 - 0.080589 36.618937)
  |   pagesize 20.0cm x 28.7cm
  |   filename /home/roel/hiking/hikingmap/test/detail.3.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test3.gpx
  Removing temp file .*hikingmap_temp_waypoints.*.gpx (re)
  $ xmllint --format $TESTDIR/tempwaypointfile.gpx | diff -uNr - $TESTDIR/test3_waypoints.xml
  $ rm -f $TESTDIR/tempwaypointfile.gpx

nowaypoints:
  $ hikingmap --debug -v -s 50000 --pagewidth 20.0 --pageheight 28.7 --pageoverlap 1.0 --overview -w 0 -o naturalorder -b $TESTDIR/detail. --gpx $TESTDIR/test3.gpx -- $TESTDIR/render-test.py
  Reading file /home/roel/hiking/hikingmap/test/test3.gpx
  Found track track 000
  => new track 0
  Found track track 001
  => new track 1
  Found track track 002
  => new track 2
  Found track track 003
  => new track 3
  Calculating track order permutation resulting in a minimum amount of pages
  This may take a while, checking 24 track permutations
  Found track permutation with 6 pages
  Found track permutation with 5 pages
  Found track permutation with 4 pages
  Page order is naturalorder
  overview map (portrait): -0.040328,36.220999 - 0.321785,36.640096, scale = 1:162420
  | Test rendering:
  |   bbox (-0.040328 36.220999 - 0.321785 36.640096)
  |   pagesize 20.0cm x 28.7cm
  |   filename /home/roel/hiking/hikingmap/test/detail.0.pdf
  |   temptrackfile = .*hikingmap_temp_overview.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test3.gpx
  detail map 1 (portrait): 0.201255,36.242158 - 0.312732,36.371175
  | Test rendering:
  |   bbox (0.201255 36.242158 - 0.312732 36.371175)
  |   pagesize 20.0cm x 28.7cm
  |   filename /home/roel/hiking/hikingmap/test/detail.1.pdf
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test3.gpx
  detail map 2 (landscape): 0.109946,36.355882 - 0.270172,36.445788
  | Test rendering:
  |   bbox (0.109946 36.355882 - 0.270172 36.445788)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.2.pdf
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test3.gpx
  detail map 3 (landscape): -0.023655,36.426579 - 0.136694,36.516486
  | Test rendering:
  |   bbox (-0.023655 36.426579 - 0.136694 36.516486)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.3.pdf
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test3.gpx
  detail map 4 (portrait): -0.031275,36.489921 - 0.080589,36.618937
  | Test rendering:
  |   bbox (-0.031275 36.489921 - 0.080589 36.618937)
  |   pagesize 20.0cm x 28.7cm
  |   filename /home/roel/hiking/hikingmap/test/detail.4.pdf
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test3.gpx
  Removing temp file .*hikingmap_temp_overview.*.gpx (re)
  $ xmllint --format $TESTDIR/tempoverviewfile.gpx | diff -uNr - $TESTDIR/test3_overview.xml
  $ rm -f $TESTDIR/tempoverviewfile.gpx

renderoptions:
  $ hikingmap --debug -v -s 50000 --pagewidth 20.0 --pageheight 28.7 --pageoverlap 1.0 --overview -w 1 -u km -o naturalorder -b $TESTDIR/detail. --gpx $TESTDIR/test3.gpx -- $TESTDIR/render-test.py --description "This is a renderoptions test"
  Reading file /home/roel/hiking/hikingmap/test/test3.gpx
  Found track track 000
  => new track 0
  Found track track 001
  => new track 1
  Found track track 002
  => new track 2
  Found track track 003
  => new track 3
  Generating waypoints for track 0: 0.115582,36.429966 - 0.113308,36.426573
  Total track distance: 0.47 km
  Generating waypoints for track 1: 0.033205,36.488041 - 0.031212,36.487269
  Total track distance: 0.20 km
  Generating waypoints for track 2: 0.261325,36.34589 - 0.264876,36.342772
  Total track distance: 0.48 km
  Generating waypoints for track 3: 0.308385,36.244406 - 0.001886,36.594681
  Total track distance: 107.84 km
  Calculating track order permutation resulting in a minimum amount of pages
  This may take a while, checking 24 track permutations
  Found track permutation with 6 pages
  Found track permutation with 5 pages
  Found track permutation with 4 pages
  Page order is naturalorder
  overview map (portrait): -0.040328,36.220999 - 0.321785,36.640096, scale = 1:162420
  | Test rendering:
  |   description This is a renderoptions test
  |   bbox (-0.040328 36.220999 - 0.321785 36.640096)
  |   pagesize 20.0cm x 28.7cm
  |   filename /home/roel/hiking/hikingmap/test/detail.0.pdf
  |   temptrackfile = .*hikingmap_temp_overview.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test3.gpx
  detail map 1 (portrait): 0.201255,36.242158 - 0.312732,36.371175
  | Test rendering:
  |   description This is a renderoptions test
  |   bbox (0.201255 36.242158 - 0.312732 36.371175)
  |   pagesize 20.0cm x 28.7cm
  |   filename /home/roel/hiking/hikingmap/test/detail.1.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test3.gpx
  detail map 2 (landscape): 0.109946,36.355882 - 0.270172,36.445788
  | Test rendering:
  |   description This is a renderoptions test
  |   bbox (0.109946 36.355882 - 0.270172 36.445788)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.2.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test3.gpx
  detail map 3 (landscape): -0.023655,36.426579 - 0.136694,36.516486
  | Test rendering:
  |   description This is a renderoptions test
  |   bbox (-0.023655 36.426579 - 0.136694 36.516486)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.3.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test3.gpx
  detail map 4 (portrait): -0.031275,36.489921 - 0.080589,36.618937
  | Test rendering:
  |   description This is a renderoptions test
  |   bbox (-0.031275 36.489921 - 0.080589 36.618937)
  |   pagesize 20.0cm x 28.7cm
  |   filename /home/roel/hiking/hikingmap/test/detail.4.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test3.gpx
  Removing temp file .*hikingmap_temp_waypoints.*.gpx (re)
  Removing temp file .*hikingmap_temp_overview.*.gpx (re)
  $ xmllint --format $TESTDIR/tempoverviewfile.gpx | diff -uNr - $TESTDIR/test3_overview.xml
  $ xmllint --format $TESTDIR/tempwaypointfile.gpx | diff -uNr - $TESTDIR/test3_waypoints.xml
  $ rm -f $TESTDIR/tempoverviewfile.gpx $TESTDIR/tempwaypointfile.gpx

test1:
  $ hikingmap --debug -v -s 50000 --pagewidth 20.0 --pageheight 28.7 --pageoverlap 1.0 --overview -w 1 -u km -o naturalorder -b $TESTDIR/detail. --gpx $TESTDIR/test1.gpx -- $TESTDIR/render-test.py
  Reading file /home/roel/hiking/hikingmap/test/test1.gpx
  Found track track 000
  => new track 0
  Found track track 001
  => new track 1
  Found track track 002
  => new track 2
  Found track track 003
  => new track 3
  Found track track 004
  => new track 4
  Found track track 005
  => new track 5
  Generating waypoints for track 0: 0.202043,50.15133 - 0.142642,50.121724
  Total track distance: 7.32 km
  Generating waypoints for track 1: 0.014733,50.23897 - 0.057488,50.2679
  Total track distance: 7.76 km
  Generating waypoints for track 2: 0.240819,50.203693 - 0.271912,50.249238
  Total track distance: 7.52 km
  Generating waypoints for track 3: 0.00058,50.242979 - 0.206156,50.196791
  Total track distance: 123.40 km
  Generating waypoints for track 4: 0.538902,50.177782 - 0.524084,50.149292
  Total track distance: 3.77 km
  Generating waypoints for track 5: 0.198391,50.197266 - 0.360945,50.137978
  Total track distance: 35.01 km
  Calculating track order permutation resulting in a minimum amount of pages
  This may take a while, checking 720 track permutations
  Found track permutation with 7 pages
  Found track permutation with 6 pages
  Page order is naturalorder
  overview map (landscape): -0.044192,50.060627 - 0.554202,50.328274, scale = 1:148846
  | Test rendering:
  |   bbox (-0.044192 50.060627 - 0.554202 50.328274)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.0.pdf
  |   temptrackfile = .*hikingmap_temp_overview.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test1.gpx
  detail map 1 (portrait): 0.102233,50.070969 - 0.242452,50.199985
  | Test rendering:
  |   bbox (0.102233 50.070969 - 0.242452 50.199985)
  |   pagesize 20.0cm x 28.7cm
  |   filename /home/roel/hiking/hikingmap/test/detail.1.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test1.gpx
  detail map 2 (portrait): -0.033767,50.188916 - 0.106803,50.317932
  | Test rendering:
  |   bbox (-0.033767 50.188916 - 0.106803 50.317932)
  |   pagesize 20.0cm x 28.7cm
  |   filename /home/roel/hiking/hikingmap/test/detail.2.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test1.gpx
  detail map 3 (landscape): 0.103441,50.15936 - 0.304983,50.249267
  | Test rendering:
  |   bbox (0.103441 50.159360 - 0.304983 50.249267)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.3.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test1.gpx
  detail map 4 (landscape): 0.297965,50.185425 - 0.499544,50.275332
  | Test rendering:
  |   bbox (0.297965 50.185425 - 0.499544 50.275332)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.4.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test1.gpx
  detail map 5 (portrait): 0.403588,50.104238 - 0.543777,50.233254
  | Test rendering:
  |   bbox (0.403588 50.104238 - 0.543777 50.233254)
  |   pagesize 20.0cm x 28.7cm
  |   filename /home/roel/hiking/hikingmap/test/detail.5.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test1.gpx
  detail map 6 (landscape): 0.224245,50.096971 - 0.425416,50.186878
  | Test rendering:
  |   bbox (0.224245 50.096971 - 0.425416 50.186878)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.6.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test1.gpx
  Removing temp file .*hikingmap_temp_waypoints.*.gpx (re)
  Removing temp file .*hikingmap_temp_overview.*.gpx (re)
  $ xmllint --format $TESTDIR/tempoverviewfile.gpx | diff -uNr - $TESTDIR/test1_overview.xml
  $ xmllint --format $TESTDIR/tempwaypointfile.gpx | diff -uNr - $TESTDIR/test1_waypoints.xml
  $ rm -f $TESTDIR/tempoverviewfile.gpx $TESTDIR/tempwaypointfile.gpx

test2:
  $ hikingmap --debug -v -s 50000 --pagewidth 20.0 --pageheight 28.7 --pageoverlap 1.0 --overview -w 1 -u km -o naturalorder -b $TESTDIR/detail. --gpx $TESTDIR/test2.gpx -- $TESTDIR/render-test.py
  Reading file /home/roel/hiking/hikingmap/test/test2.gpx
  Found track track 000
  => new track 0
  Found track track 001
  => connecting after track 0
  Found track track 002
  => connecting after track 0
  Generating waypoints for track 0: 3.038883,46.976688 - 0.00162,46.939971
  Total track distance: 420.44 km
  Calculating track order permutation resulting in a minimum amount of pages
  This may take a while, checking 1 track permutations
  Found track permutation with 20 pages
  Page order is naturalorder
  overview map (landscape): -0.105699,45.969392 - 3.100815,47.507834, scale = 1:855575
  | Test rendering:
  |   bbox (-0.105699 45.969392 - 3.100815 47.507834)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.00.pdf
  |   temptrackfile = .*hikingmap_temp_overview.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test2.gpx
  detail map 1 (portrait): 2.913442,46.859148 - 3.044953,46.988164
  | Test rendering:
  |   bbox (2.913442 46.859148 - 3.044953 46.988164)
  |   pagesize 20.0cm x 28.7cm
  |   filename /home/roel/hiking/hikingmap/test/detail.01.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test2.gpx
  detail map 2 (landscape): 2.731619,46.821583 - 2.920285,46.91149
  | Test rendering:
  |   bbox (2.731619 46.821583 - 2.920285 46.911490)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.02.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test2.gpx
  detail map 3 (landscape): 2.549903,46.824685 - 2.738545,46.914592
  | Test rendering:
  |   bbox (2.549903 46.824685 - 2.738545 46.914592)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.03.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test2.gpx
  detail map 4 (landscape): 2.368143,46.82757 - 2.556787,46.917477
  | Test rendering:
  |   bbox (2.368143 46.827570 - 2.556787 46.917477)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.04.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test2.gpx
  detail map 5 (landscape): 2.186385,46.813611 - 2.374967,46.903518
  | Test rendering:
  |   bbox (2.186385 46.813611 - 2.374967 46.903518)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.05.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test2.gpx
  detail map 6 (portrait): 2.061927,46.717334 - 2.193098,46.84635
  | Test rendering:
  |   bbox (2.061927 46.717334 - 2.193098 46.846350)
  |   pagesize 20.0cm x 28.7cm
  |   filename /home/roel/hiking/hikingmap/test/detail.06.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test2.gpx
  detail map 7 (landscape): 1.880532,46.675504 - 2.068597,46.765411
  | Test rendering:
  |   bbox (1.880532 46.675504 - 2.068597 46.765411)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.07.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test2.gpx
  detail map 8 (landscape): 1.699357,46.630551 - 1.887327,46.720458
  | Test rendering:
  |   bbox (1.699357 46.630551 - 1.887327 46.720458)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.08.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test2.gpx
  detail map 9 (portrait): 1.57642,46.536709 - 1.707125,46.665726
  | Test rendering:
  |   bbox (1.576420 46.536709 - 1.707125 46.665726)
  |   pagesize 20.0cm x 28.7cm
  |   filename /home/roel/hiking/hikingmap/test/detail.09.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test2.gpx
  detail map 10 (landscape): 1.414669,46.489845 - 1.602169,46.579752
  | Test rendering:
  |   bbox (1.414669 46.489845 - 1.602169 46.579752)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.10.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test2.gpx
  detail map 11 (landscape): 1.233674,46.50066 - 1.421204,46.590567
  | Test rendering:
  |   bbox (1.233674 46.500660 - 1.421204 46.590567)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.11.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test2.gpx
  detail map 12 (landscape): 1.05258,46.521235 - 1.24021,46.611142
  | Test rendering:
  |   bbox (1.052580 46.521235 - 1.240210 46.611142)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.12.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test2.gpx
  detail map 13 (landscape): 0.871724,46.504966 - 1.059282,46.594872
  | Test rendering:
  |   bbox (0.871724 46.504966 - 1.059282 46.594872)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.13.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test2.gpx
  detail map 14 (landscape): 0.691087,46.489062 - 0.878589,46.578969
  | Test rendering:
  |   bbox (0.691087 46.489062 - 0.878589 46.578969)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.14.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test2.gpx
  detail map 15 (landscape): 0.51297,46.54294 - 0.700554,46.632847
  | Test rendering:
  |   bbox (0.512970 46.542940 - 0.700554 46.632847)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.15.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test2.gpx
  detail map 16 (landscape): 0.3344,46.615553 - 0.522278,46.70546
  | Test rendering:
  |   bbox (0.334400 46.615553 - 0.522278 46.705460)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.16.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test2.gpx
  detail map 17 (landscape): 0.171435,46.671978 - 0.359523,46.761885
  | Test rendering:
  |   bbox (0.171435 46.671978 - 0.359523 46.761885)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.17.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test2.gpx
  detail map 18 (portrait): 0.105102,46.718433 - 0.236247,46.84745
  | Test rendering:
  |   bbox (0.105102 46.718433 - 0.236247 46.847450)
  |   pagesize 20.0cm x 28.7cm
  |   filename /home/roel/hiking/hikingmap/test/detail.18.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test2.gpx
  detail map 19 (landscape): 0.028638,46.831428 - 0.217265,46.921335
  | Test rendering:
  |   bbox (0.028638 46.831428 - 0.217265 46.921335)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.19.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test2.gpx
  detail map 20 (portrait): -0.049837,46.8587 - 0.081761,46.987716
  | Test rendering:
  |   bbox (-0.049837 46.858700 - 0.081761 46.987716)
  |   pagesize 20.0cm x 28.7cm
  |   filename /home/roel/hiking/hikingmap/test/detail.20.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test2.gpx
  Removing temp file .*hikingmap_temp_waypoints.*.gpx (re)
  Removing temp file .*hikingmap_temp_overview.*.gpx (re)
  $ xmllint --format $TESTDIR/tempoverviewfile.gpx | diff -uNr - $TESTDIR/test2_overview.xml
  $ xmllint --format $TESTDIR/tempwaypointfile.gpx | diff -uNr - $TESTDIR/test2_waypoints.xml
  $ rm -f $TESTDIR/tempoverviewfile.gpx $TESTDIR/tempwaypointfile.gpx

test3:
  $ hikingmap --debug -v -s 50000 --pagewidth 20.0 --pageheight 28.7 --pageoverlap 1.0 --overview -w 1 -u km -o naturalorder -b $TESTDIR/detail. --gpx $TESTDIR/test3.gpx -- $TESTDIR/render-test.py
  Reading file /home/roel/hiking/hikingmap/test/test3.gpx
  Found track track 000
  => new track 0
  Found track track 001
  => new track 1
  Found track track 002
  => new track 2
  Found track track 003
  => new track 3
  Generating waypoints for track 0: 0.115582,36.429966 - 0.113308,36.426573
  Total track distance: 0.47 km
  Generating waypoints for track 1: 0.033205,36.488041 - 0.031212,36.487269
  Total track distance: 0.20 km
  Generating waypoints for track 2: 0.261325,36.34589 - 0.264876,36.342772
  Total track distance: 0.48 km
  Generating waypoints for track 3: 0.308385,36.244406 - 0.001886,36.594681
  Total track distance: 107.84 km
  Calculating track order permutation resulting in a minimum amount of pages
  This may take a while, checking 24 track permutations
  Found track permutation with 6 pages
  Found track permutation with 5 pages
  Found track permutation with 4 pages
  Page order is naturalorder
  overview map (portrait): -0.040328,36.220999 - 0.321785,36.640096, scale = 1:162420
  | Test rendering:
  |   bbox (-0.040328 36.220999 - 0.321785 36.640096)
  |   pagesize 20.0cm x 28.7cm
  |   filename /home/roel/hiking/hikingmap/test/detail.0.pdf
  |   temptrackfile = .*hikingmap_temp_overview.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test3.gpx
  detail map 1 (portrait): 0.201255,36.242158 - 0.312732,36.371175
  | Test rendering:
  |   bbox (0.201255 36.242158 - 0.312732 36.371175)
  |   pagesize 20.0cm x 28.7cm
  |   filename /home/roel/hiking/hikingmap/test/detail.1.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test3.gpx
  detail map 2 (landscape): 0.109946,36.355882 - 0.270172,36.445788
  | Test rendering:
  |   bbox (0.109946 36.355882 - 0.270172 36.445788)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.2.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test3.gpx
  detail map 3 (landscape): -0.023655,36.426579 - 0.136694,36.516486
  | Test rendering:
  |   bbox (-0.023655 36.426579 - 0.136694 36.516486)
  |   pagesize 28.7cm x 20.0cm
  |   filename /home/roel/hiking/hikingmap/test/detail.3.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test3.gpx
  detail map 4 (portrait): -0.031275,36.489921 - 0.080589,36.618937
  | Test rendering:
  |   bbox (-0.031275 36.489921 - 0.080589 36.618937)
  |   pagesize 20.0cm x 28.7cm
  |   filename /home/roel/hiking/hikingmap/test/detail.4.pdf
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = /home/roel/hiking/hikingmap/test/test3.gpx
  Removing temp file .*hikingmap_temp_waypoints.*.gpx (re)
  Removing temp file .*hikingmap_temp_overview.*.gpx (re)
  $ xmllint --format $TESTDIR/tempoverviewfile.gpx | diff -uNr - $TESTDIR/test3_overview.xml
  $ xmllint --format $TESTDIR/tempwaypointfile.gpx | diff -uNr - $TESTDIR/test3_waypoints.xml
  $ rm -f $TESTDIR/tempoverviewfile.gpx $TESTDIR/tempwaypointfile.gpx

