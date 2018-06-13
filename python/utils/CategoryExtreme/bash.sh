
cat test.txt | tail -n +1 | python3 CategoryExtremeV2.py -k2 -v 3 --txt --min
#1       Title   t
#2       ss      1
#4       s1      0
#5       s2      4              

cat test.txt | tail -n +2 | python3 CategoryExtremeV2.py -k2 -v 3 --max -a
#3       ss      3
#4       ss      3
#4       s1      1
#5       s2      4

cat test.txt | tail -n +2 | python3 CategoryExtremeV2.py -k2 -v 3 -o 4,3,2,1,0 --max
#2       ss      1
#4       s1      0
#5       s2      4
