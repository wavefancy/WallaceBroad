
# Test the range set as (], left open.
cat test.txt | python3 ./Continuous2Categorical.py   -c X -n D -b 1,2,10 -l A,B
#X       D
#1       NA
#2       A
#NA      NA
#3       B
#4       B

# Auto detect min or max.
cat test.txt | python3 ./Continuous2Categorical.py  -c X -n M -b m,2,m -l A,B
#X       M
#1       A
#2       A
#NA      NA
#3       B
#4       B

# Test using the percentile to specify cut-off.
cat test.txt | python3 ./Continuous2Categorical.py  -c X -n M -p m,0.49,m -l A,B
#X       M
#1       A
#2       A
#NA      NA
#3       B
#4       B
