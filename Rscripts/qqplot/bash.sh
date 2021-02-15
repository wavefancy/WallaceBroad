
wecho "
    cat test.txt | /Users/minxian/Broad/Program/miniconda3/envs/forestplot2/bin/Rscript
        qqplot.R -o test.pdf -g G7,G6 --xlim 0,1 --sy 2 --ylim 0,11 --yb 0,2,4,6,8,10 --ybl 0,2,4,6,8,19 --tp 1E-4
            -H 3 -W 3
        --l 0.7::2::1.58
"
