wecho "
    cat test.txt | Rscript ggScattterPlot.R -x 'X1' -y Y
        -o test.pdf -W 3 -H 3
        -c C
        --cl 'B::C::A'
        #--sp C
        --cp '#00AFBB::#E7B800::#FC4E07'
        # custom the location for legend.
        -l 'c(0.5,0.5)'
        --lt noshow --lfs 10
        -a 1 -s 5
        --xlim 0,10
        --gl
        --gls 1
        --rx '-45'
        --xb '1,3,5'
        --xl 'A,B,C'
        --xlab 'myx' --ylab 'myy'
        --ylim 0,30
"
