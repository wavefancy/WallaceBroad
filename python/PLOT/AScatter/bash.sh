wecho "
    cat test.txt | python3 AScatter.py -x X -y Y -s Z | vl2svg /dev/stdin >test.svg
    #&& convert -density 300 test.svg test.jpg
"
