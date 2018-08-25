
cat test.txt | python3 AlignGWASBeta.py -a 1,2,4,5 -b 3,6

#A       T       -1      T       A       -1      AMBIGUOUS
#A       G       -1      A       G       -2.0    OK
#A       C       -1      A       C       2       OK
#A       C       -1      A       C       -2.0    OK
## comments
#A       G       -1      T       A       2       FAIL
