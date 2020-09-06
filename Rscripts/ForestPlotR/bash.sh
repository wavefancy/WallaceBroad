# Test for line header has two lines.
# Have to make every column to show has two lines.
 cat ./two_line_title_group.txt | Rscript ./ForestPlot.Middle.R -o two_line_title_group.pdf -W 9 -H 4.5 -g GROUP && open two_line_title_group.pdf
 cat ./two_line_title_group.txt | Rscript ./ForestPlot.Middle.R -o two_line_title_group_xlim.pdf -W 9 -H 4.5 -g GROUP --xlim 1::20 --rp '_n_OR[95CI]::_n_PVALUE' && open two_line_title_group_xlim.pdf
 cat ./two_line_title_nogroup.txt | Rscript ./ForestPlot.Middle.R -o two_line_title_nogroup.pdf -W 9 -H 2.5 && open two_line_title_nogroup.pdf
 cat ./two_line_title_nogroup.txt | Rscript ./ForestPlot.Middle.R -o two_line_title_nogroup_m.pdf -W 9 -H 2.5 --rp '_n_OR[95CI]::_n_PVALUE' --xr 0.55::0.25 && open two_line_title_nogroup_m.pdf
 cat ./one_line_title_nogroup.txt | Rscript ./ForestPlot.Middle.R -o one_line_title_nogroup.pdf -W 12 -H 3 && open one_line_title_nogroup.pdf
 cat ./one_line_title_nogroup.txt | Rscript ./ForestPlot.Middle.R -o one_line_title_nogroup_m.pdf -W 12 -H 3 --rp 'OR[95CI]::PVALUE' && open one_line_title_nogroup_m.pdf
