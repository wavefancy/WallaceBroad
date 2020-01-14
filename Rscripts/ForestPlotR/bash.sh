# Test for line header has two lines.
# Have to make every column to show has two lines.
# cat forest.middle-wgs.txt | Rscript ./ForestPlot.R -o test.pdf -W 9 -H 4.5 -g GROUP
cat forest.middle_UKB_V2_sw.txt | Rscript ./ForestPlot.R -o test_UKB_sw.pdf -W 9 -H 4.5 -g GROUP
cat forest.middle_UKB_V2_ws.txt | Rscript ./ForestPlot.R -o test_UKB_ws.pdf -W 9 -H 4.5 -g GROUP --xlim 0,2.5
