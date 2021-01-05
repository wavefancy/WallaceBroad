
wecho "
    cat ./test.tsv
    | /Users/minxian/Broad/Program/miniconda3/envs/edger/bin/Rscript
        ./GLMCovariateLRTest.R
        -c <(cat ./cov.csv | wcut -f1- -d ',')
        -b 'SCORE~TIME+GENO+iCPMsum+TIME*GENO'
        -s 'SCORE~TIME+GENO+iCPMsum'
        -i NAME
        --dc 3
    > test.out.tsv
"
