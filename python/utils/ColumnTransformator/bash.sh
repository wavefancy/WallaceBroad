wecho "
    cat in.txt | python3 ./ColumnTransformator.py -c 2 -t maf
"
#1       0.1000
#2       -2.0000
#3       0.2000

wecho "
    cat ./in.p2v.2sided.txt | python3 ./ColumnTransformator.py -c ZfromP -t P2Z:Z
"
