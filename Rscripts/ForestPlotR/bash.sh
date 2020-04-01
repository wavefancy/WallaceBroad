# Test for line header has two lines.
# Have to make every column to show has two lines.
 cat ./two_line_title_group.txt | Rscript ./ForestPlot.R -o two_line_title_group.pdf -W 9 -H 4.5 -g GROUP && open two_line_title_group.pdf
 cat ./two_line_title_nogroup.txt | Rscript ./ForestPlot.R -o two_line_title_nogroup.pdf -W 9 -H 2.5 && open two_line_title_nogroup.pdf
 cat ./one_line_title_nogroup.txt | Rscript ./ForestPlot.R -o one_line_title_nogroup.pdf -W 12 -H 3 && open one_line_title_nogroup.pdf
