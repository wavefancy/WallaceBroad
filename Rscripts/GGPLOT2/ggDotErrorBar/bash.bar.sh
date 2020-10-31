wecho "
    #cat ./test.txt | Rscript ./ggDotErrorBar.R
    cat ./temp.txt | /Users/minxian/Broad/Program/miniconda3/envs/forestplot/bin/Rscript ./ggBarDotErrorBar.R
        -x dose -y len
        --ymin ymi --ymax yma
        --xlab myx --ylab myy
        -l 'right'
        -c supp
        -H 5 -W 5
        --cp '#00AFBB::#E7B800::#FC4E07'
        #--cp 'black::white'
        --js 0.7
        --bar
        --gt ymi
        --ec 'lightblue'
        -o test.bar.pdf
        --ylim 5,30
        #--logy log2
        #--yticks 5,10,20
"
