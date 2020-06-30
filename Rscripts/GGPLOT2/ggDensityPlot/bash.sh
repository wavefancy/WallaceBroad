gunzip -dc test.txt.gz | Rscript ggDensityPlot.R -x weight -o test-sex.png -W 5 -H 3 -c sex --cp 'red::black' --xlab myx -l 'c(0.5,0.5)' && open test-sex.png
gunzip -dc test.txt.gz | Rscript ggDensityPlot.R -x weight -o test-sex.pdf -W 5 -H 3 -c sex --cp Dark2
gunzip -dc test.txt.gz | Rscript ggDensityPlot.R -x weight -o test.pdf -W 5 -H 3
gunzip -dc test.txt.gz | Rscript ggDensityPlot.R -x weight -o test-sex.pdf -W 5 -H 3 -c sex --cp Dark2 --xlim 50,100 --ylim 0,1
