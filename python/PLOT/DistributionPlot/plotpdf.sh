
cat test.txt | python3 DistributionPlotV2.py -x myx -o temp-plot.html -t --cl red\
&& phantomjs ~/scripts/js/rasterize.js temp-plot.html test.pdf 10in*5in \
&& display test.pdf
