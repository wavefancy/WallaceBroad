
wecho "
    cat test.c2.txt | python3 BoxPlot.py --c2 -x myx -y EUR_ANC% -o temp-plot.html
    #--ha '0_1_0.8_*' --haw 1.5
    --ms 5
    ##--nobox
&& phantomjs ~/scripts/js/rasterize.js temp-plot.html test.pdf 10in*5in
&& open test.pdf
"
