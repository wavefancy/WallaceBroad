
cat test.txt | python3 SubsetByKey.py -v 3,1 -c 2 -k

##12     3
#A       1
#B       1

cat test.txt | python3 SubsetByKey.py -v 5,1 -c 2 -k -m --cs '#1'
##12     3
#TITLE   5
#A       1
#B       1
