wecho "
    cat test.txt | Rscript ggScattterPlot.R -x X -y Y
        -o test.pdf -W 3 -H 3
        -c red
        --sp C
        --cp '#00AFBB::#E7B800::#FC4E07'
        # custom the location for legend.
        -l 'c(0.8,0.8)'
        --lt noshow --lfs 10
        -a 1 -s 5
        --xlim 0,10
"