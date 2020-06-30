gunzip -dc test.txt.gz | Rscript ggDensityPlot.R -x weight -o test-sex.png -W 5 -H 3 -c sex -p Dark2 --xlab myx && open test-sex.png
gunzip -dc test.txt.gz | Rscript ggDensityPlot.R -x weight -o test-sex.pdf -W 5 -H 3 -c sex -p Dark2
gunzip -dc test.txt.gz | Rscript ggDensityPlot.R -x weight -o test.pdf -W 5 -H 3
gunzip -dc test.txt.gz | Rscript ggDensityPlot.R -x weight -o test-sex.pdf -W 5 -H 3 -c sex -p Dark2 --xlim 50,100 --ylim 0,1
