
#zcat all.group.idp.gz | grep -v case | python3 BoxPlot.py -x myx -y myy -o temp-plot.html\
wecho "
    gzcat all.group.idp.gz | grep -v case | python3 BoxPlot.py -x myx -y EUR_ANC% -o temp-plot.html --ha '0_1_0.8_*' --haw 1.5 --nooutliers --atext 0_0.4_Mean,1_0.4_Median --atr -45
    && phantomjs ~/scripts/js/rasterize.js temp-plot.html test.pdf 10in*5in
    && open test.pdf
"
