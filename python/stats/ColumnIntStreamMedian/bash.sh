
cat test.txt | sed 's|10|nan|' | python ColumnIntStreamMedian.py

#STATS   A       B       C
#MEDIAN  0.5     2       3.5
