
cat test.txt | python3 ShadePlot.py -x position -y density -o temp-plot.html --sa 3,5 --y2 y2titletest --lm 100 --ms 5 --lw 1 --y2d 0.5 --y1d 1 --y2r 0,7 --yr 0,15 --y2c black --rm 100 --xdt 2 \
&& phantomjs ~/scripts/js/rasterize.js temp-plot.html test.pdf 8in*3in \
&& display test.pdf
