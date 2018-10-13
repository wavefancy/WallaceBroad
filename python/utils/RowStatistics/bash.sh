
cat test.txt | python3 ./RowStatistics.py -c --set 10 --min 2 --max 2 --mean --median --std --nvalid

#NAME    N_VALID MEAN    MEDIAN  STD     MIN_2   MAX_2   SET_10
#N1      3       2.0000e+00      2.0000e+00      8.1650e-01      1.0,2.0 2.0,3.0 1,2,3
#N2      4       2.7500e+00      2.5000e+00      1.7854e+00      1.0,4.0 4.0,5.0 1,4,5
#N3      0       NA      NA      NA      NA      NA      a,b,c
