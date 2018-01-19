<<<<<<< HEADcat test.txt | python3 GCCategorySummay.py
#Label   correct_00      correct_01      correct_11      error_00        error_01        error_11        errorRate_00   errorRate_01    errorRate_1     errorRate_Total
#T       76      2       0       0       2       0       0.0000e+00      5.0000e-01      NA      2.5000e-02
#A       114     2       0       1       0       1       8.6957e-03      0.0000e+00      1.0000e+00      1.6949e-02


cat test.txt | python3 GenotypeConcordance.py -s names.txt -c 2 -i

#true_sample	call_sample	correct_00	correct_01	correct_11	error_00	error_01	error_11	errorRate_00	errorRate_01	errorRate_11	errorRateTotal
#s1	s3	0	1	1	0	1	0	NA	5.0000e-01	0.0000e+00	3.3333e-01
#s2	s4	4	0	1	0	0	0	0.0000e+00	NA	0.0000e+00	0.0000e+00
