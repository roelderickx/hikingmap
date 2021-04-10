  $ [ "$0" != "/bin/bash" ] || shopt -s expand_aliases
  $ [ -n "$PYTHON" ] || PYTHON="`which python`"
  $ alias hikingmap="TMPDIR=$TESTDIR PYTHONPATH=$TESTDIR/.. $PYTHON -m hikingmap"

rectoversoorder:
  $ hikingmap --debug -v -s 50000 --pagewidth 20.0 --pageheight 28.7 --pageoverlap 1.0 --overview -w 1 -u km -o rectoverso -b $TESTDIR/detail. --gpx $TESTDIR/test2.gpx -- $TESTDIR/render-test.py
  Reading file .*/hikingmap/test/test2.gpx (re)
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
  Page order is rectoverso, new order = 0 10 1 11 2 12 3 13 4 14 5 15 6 16 7 17 8 18 9 19 20
  overview map (landscape): -0.105699,45.969392 - 3.100815,47.507834, scale = 1:855575
  | Test rendering:
  |   bbox (-0.105699 45.969392 - 3.100815 47.507834)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.00.pdf (re)
  |   temptrackfile = .*hikingmap_temp_overview.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 10 (landscape): 1.414669,46.489845 - 1.602169,46.579752
  | Test rendering:
  |   bbox (1.414669 46.489845 - 1.602169 46.579752)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.01.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 1 (portrait): 2.913442,46.859148 - 3.044953,46.988164
  | Test rendering:
  |   bbox (2.913442 46.859148 - 3.044953 46.988164)
  |   pagesize 20.0cm x 28.7cm
  |   filename .*/hikingmap/test/detail.02.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 11 (landscape): 1.233674,46.50066 - 1.421204,46.590567
  | Test rendering:
  |   bbox (1.233674 46.500660 - 1.421204 46.590567)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.03.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 2 (landscape): 2.731619,46.821583 - 2.920285,46.91149
  | Test rendering:
  |   bbox (2.731619 46.821583 - 2.920285 46.911490)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.04.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 12 (landscape): 1.05258,46.521235 - 1.24021,46.611142
  | Test rendering:
  |   bbox (1.052580 46.521235 - 1.240210 46.611142)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.05.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 3 (landscape): 2.549903,46.824685 - 2.738545,46.914592
  | Test rendering:
  |   bbox (2.549903 46.824685 - 2.738545 46.914592)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.06.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 13 (landscape): 0.871724,46.504966 - 1.059282,46.594872
  | Test rendering:
  |   bbox (0.871724 46.504966 - 1.059282 46.594872)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.07.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 4 (landscape): 2.368143,46.82757 - 2.556787,46.917477
  | Test rendering:
  |   bbox (2.368143 46.827570 - 2.556787 46.917477)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.08.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 14 (landscape): 0.691087,46.489062 - 0.878589,46.578969
  | Test rendering:
  |   bbox (0.691087 46.489062 - 0.878589 46.578969)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.09.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 5 (landscape): 2.186385,46.813611 - 2.374967,46.903518
  | Test rendering:
  |   bbox (2.186385 46.813611 - 2.374967 46.903518)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.10.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 15 (landscape): 0.51297,46.54294 - 0.700554,46.632847
  | Test rendering:
  |   bbox (0.512970 46.542940 - 0.700554 46.632847)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.11.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 6 (portrait): 2.061927,46.717334 - 2.193098,46.84635
  | Test rendering:
  |   bbox (2.061927 46.717334 - 2.193098 46.846350)
  |   pagesize 20.0cm x 28.7cm
  |   filename .*/hikingmap/test/detail.12.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 16 (landscape): 0.3344,46.615553 - 0.522278,46.70546
  | Test rendering:
  |   bbox (0.334400 46.615553 - 0.522278 46.705460)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.13.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 7 (landscape): 1.880532,46.675504 - 2.068597,46.765411
  | Test rendering:
  |   bbox (1.880532 46.675504 - 2.068597 46.765411)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.14.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 17 (landscape): 0.171435,46.671978 - 0.359523,46.761885
  | Test rendering:
  |   bbox (0.171435 46.671978 - 0.359523 46.761885)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.15.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 8 (landscape): 1.699357,46.630551 - 1.887327,46.720458
  | Test rendering:
  |   bbox (1.699357 46.630551 - 1.887327 46.720458)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.16.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 18 (portrait): 0.105102,46.718433 - 0.236247,46.84745
  | Test rendering:
  |   bbox (0.105102 46.718433 - 0.236247 46.847450)
  |   pagesize 20.0cm x 28.7cm
  |   filename .*/hikingmap/test/detail.17.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 9 (portrait): 1.57642,46.536709 - 1.707125,46.665726
  | Test rendering:
  |   bbox (1.576420 46.536709 - 1.707125 46.665726)
  |   pagesize 20.0cm x 28.7cm
  |   filename .*/hikingmap/test/detail.18.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 19 (landscape): 0.028638,46.831428 - 0.217265,46.921335
  | Test rendering:
  |   bbox (0.028638 46.831428 - 0.217265 46.921335)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.19.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 20 (portrait): -0.049837,46.8587 - 0.081761,46.987716
  | Test rendering:
  |   bbox (-0.049837 46.858700 - 0.081761 46.987716)
  |   pagesize 20.0cm x 28.7cm
  |   filename .*/hikingmap/test/detail.20.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  Removing temp file .*hikingmap_temp_waypoints.*.gpx (re)
  Removing temp file .*hikingmap_temp_overview.*.gpx (re)
  $ xmllint --format $TESTDIR/tempoverviewfile.gpx | diff -uNr - $TESTDIR/test2_overview.xml
  $ xmllint --format $TESTDIR/tempwaypointfile.gpx | diff -uNr - $TESTDIR/test2_waypoints.xml
  $ rm -f $TESTDIR/tempoverviewfile.gpx $TESTDIR/tempwaypointfile.gpx

bookorder:
  $ hikingmap --debug -v -s 50000 --pagewidth 20.0 --pageheight 28.7 --pageoverlap 1.0 --overview -w 1 -u km -o book -b $TESTDIR/detail. --gpx $TESTDIR/test2.gpx -- $TESTDIR/render-test.py
  Reading file .*/hikingmap/test/test2.gpx (re)
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
  Page order is book, new order = X 0 1 X X 2 3 20 19 4 5 18 17 6 7 16 15 8 9 14 13 10 11 12
  WARNING: blank pages are not generated!
  overview map (landscape): -0.105699,45.969392 - 3.100815,47.507834, scale = 1:855575
  | Test rendering:
  |   bbox (-0.105699 45.969392 - 3.100815 47.507834)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.01.pdf (re)
  |   temptrackfile = .*hikingmap_temp_overview.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 1 (portrait): 2.913442,46.859148 - 3.044953,46.988164
  | Test rendering:
  |   bbox (2.913442 46.859148 - 3.044953 46.988164)
  |   pagesize 20.0cm x 28.7cm
  |   filename .*/hikingmap/test/detail.02.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 2 (landscape): 2.731619,46.821583 - 2.920285,46.91149
  | Test rendering:
  |   bbox (2.731619 46.821583 - 2.920285 46.911490)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.05.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 3 (landscape): 2.549903,46.824685 - 2.738545,46.914592
  | Test rendering:
  |   bbox (2.549903 46.824685 - 2.738545 46.914592)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.06.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 20 (portrait): -0.049837,46.8587 - 0.081761,46.987716
  | Test rendering:
  |   bbox (-0.049837 46.858700 - 0.081761 46.987716)
  |   pagesize 20.0cm x 28.7cm
  |   filename .*/hikingmap/test/detail.07.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 19 (landscape): 0.028638,46.831428 - 0.217265,46.921335
  | Test rendering:
  |   bbox (0.028638 46.831428 - 0.217265 46.921335)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.08.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 4 (landscape): 2.368143,46.82757 - 2.556787,46.917477
  | Test rendering:
  |   bbox (2.368143 46.827570 - 2.556787 46.917477)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.09.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 5 (landscape): 2.186385,46.813611 - 2.374967,46.903518
  | Test rendering:
  |   bbox (2.186385 46.813611 - 2.374967 46.903518)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.10.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 18 (portrait): 0.105102,46.718433 - 0.236247,46.84745
  | Test rendering:
  |   bbox (0.105102 46.718433 - 0.236247 46.847450)
  |   pagesize 20.0cm x 28.7cm
  |   filename .*/hikingmap/test/detail.11.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 17 (landscape): 0.171435,46.671978 - 0.359523,46.761885
  | Test rendering:
  |   bbox (0.171435 46.671978 - 0.359523 46.761885)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.12.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 6 (portrait): 2.061927,46.717334 - 2.193098,46.84635
  | Test rendering:
  |   bbox (2.061927 46.717334 - 2.193098 46.846350)
  |   pagesize 20.0cm x 28.7cm
  |   filename .*/hikingmap/test/detail.13.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 7 (landscape): 1.880532,46.675504 - 2.068597,46.765411
  | Test rendering:
  |   bbox (1.880532 46.675504 - 2.068597 46.765411)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.14.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 16 (landscape): 0.3344,46.615553 - 0.522278,46.70546
  | Test rendering:
  |   bbox (0.334400 46.615553 - 0.522278 46.705460)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.15.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 15 (landscape): 0.51297,46.54294 - 0.700554,46.632847
  | Test rendering:
  |   bbox (0.512970 46.542940 - 0.700554 46.632847)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.16.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 8 (landscape): 1.699357,46.630551 - 1.887327,46.720458
  | Test rendering:
  |   bbox (1.699357 46.630551 - 1.887327 46.720458)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.17.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 9 (portrait): 1.57642,46.536709 - 1.707125,46.665726
  | Test rendering:
  |   bbox (1.576420 46.536709 - 1.707125 46.665726)
  |   pagesize 20.0cm x 28.7cm
  |   filename .*/hikingmap/test/detail.18.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 14 (landscape): 0.691087,46.489062 - 0.878589,46.578969
  | Test rendering:
  |   bbox (0.691087 46.489062 - 0.878589 46.578969)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.19.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 13 (landscape): 0.871724,46.504966 - 1.059282,46.594872
  | Test rendering:
  |   bbox (0.871724 46.504966 - 1.059282 46.594872)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.20.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 10 (landscape): 1.414669,46.489845 - 1.602169,46.579752
  | Test rendering:
  |   bbox (1.414669 46.489845 - 1.602169 46.579752)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.21.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 11 (landscape): 1.233674,46.50066 - 1.421204,46.590567
  | Test rendering:
  |   bbox (1.233674 46.500660 - 1.421204 46.590567)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.22.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  detail map 12 (landscape): 1.05258,46.521235 - 1.24021,46.611142
  | Test rendering:
  |   bbox (1.052580 46.521235 - 1.240210 46.611142)
  |   pagesize 28.7cm x 20.0cm
  |   filename .*/hikingmap/test/detail.23.pdf (re)
  |   tempwaypointfile = .*hikingmap_temp_waypoints.*.gpx (re)
  |   gpxfiles = .*/hikingmap/test/test2.gpx (re)
  Removing temp file .*hikingmap_temp_waypoints.*.gpx (re)
  Removing temp file .*hikingmap_temp_overview.*.gpx (re)
  $ xmllint --format $TESTDIR/tempoverviewfile.gpx | diff -uNr - $TESTDIR/test2_overview.xml
  $ xmllint --format $TESTDIR/tempwaypointfile.gpx | diff -uNr - $TESTDIR/test2_waypoints.xml
  $ rm -f $TESTDIR/tempoverviewfile.gpx $TESTDIR/tempwaypointfile.gpx

