
wecho "
diff <(cat test.txt | python ColumnIntStreamMedian.py     | tail -n +2 | wcut -f2-)
     <(cat test.txt |  wcut -f1- | datamash -H median 1-3 | tail -n +2)
"
