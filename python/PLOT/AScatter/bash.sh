wecho "
    cat test.txt | python3 AScatter.py -x X -y Y -s Z
        -H 100 -W 100
        --abline 0_0_4_4
    | vl2svg /dev/stdin >test.svg
    #&& convert -density 300 test.svg test.jpg
"
