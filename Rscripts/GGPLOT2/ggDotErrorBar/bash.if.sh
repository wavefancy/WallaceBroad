xo=`cat if.csv | tail -n +2 | wcut -f1 -d ',' | Transpose.py | wcut -f1- --od '::'`
wecho "
    #cat ./test.txt | Rscript ./ggDotErrorBar.R
    cat ./if.csv
        | /Users/minxian/Broad/Program/miniconda3/envs/forestplot/bin/Rscript
            ./ggBarDotErrorBar.R
        -x 'Impact Factor Category' -y '#Papers'
        -c 'Impact Factor Category'
        --xo '$xo'
        -l 'none'
        -H 1.5 -W 3.5
        #--cp '#00AFBB::#E7B800::#FC4E07'
        --js 0.7
        --bar
        --nb
        -o if.pdf
"
