cat test.bar.txt | wcut -f1- | Rscript ggBarPlot.R -x x -y v -o bar.pdf -W 2 -H 3 --ymin vmin --ymax vmax
