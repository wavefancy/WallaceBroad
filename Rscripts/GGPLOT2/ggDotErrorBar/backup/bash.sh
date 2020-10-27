wecho "
    #cat ./test.txt | Rscript ./ggDotErrorBar.R
    cat ./temp.txt | /Users/minxian/Broad/Program/miniconda3/envs/forestplot/bin/Rscript ./ggBarDotErrorBar.R
        -x dose -y len --ymin ymi --ymax yma
        --xlab myx --ylab myy
        -l 'right'
        -c supp
        -H 5 -W 5
        --cp '#00AFBB::#E7B800::#FC4E07'
        --xo '1::2::0.5'
        --dot
        -o test.pdf
        #--ylim 3,50
        #--logy log2
        #--yticks 5,10,20
"
