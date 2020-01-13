# Test for line header has two lines.
# Have to make every column to show has two lines.
cat forest.middle-wgs.txt | Rscript ./ForestPlot.R -o test.pdf -W 9 -H 4.5 -g GROUP
