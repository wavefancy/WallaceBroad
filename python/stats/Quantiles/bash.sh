cat test.txt | python3 Quantiles.py -c 1 -a 4
#80.000000

cat test.txt | python3 Quantiles.py -c 1 -p 0.1 0.95
#Quantile        Value
#0.1     1
#0.95    5

cat test.txt | python3 Quantiles.py -c 1 -r ref.txt
#1       10
#2       20
#3       30
#4       40
#5       50
