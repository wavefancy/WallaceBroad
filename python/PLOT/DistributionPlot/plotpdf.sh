
cat test.txt | python3 DistributionPlot.py -x myx -o temp-plot.html -t\
&& phantomjs ~/scripts/js/rasterize.js temp-plot.html test.pdf 10in*5in \
&& display test.pdf
