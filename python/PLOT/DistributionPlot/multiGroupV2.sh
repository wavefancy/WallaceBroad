# Multiple group, no show histogram bar.

cat test.txt | python3 DistributionPlot.py -x myx -o temp-plot.html --hhist -p -l\
&& phantomjs ~/scripts/js/rasterize.js temp-plot.html test.mg.pdf 6in*3in \
&& display test.mg.pdf
#-t --an '0_0_test_red,0.5_0.5_test2_blue_50' --bs 0.1 --xdt 0.5 --ydt 0.2 --nc --yr 0,0.5\
