
cat test.txt | python3 ./CategoryMergeRecords.py -k 1
#1       x,y     c
#2       1       t,m

# Test empty file
echo '' | python3 ./CategoryMergeRecords.py -k 1
