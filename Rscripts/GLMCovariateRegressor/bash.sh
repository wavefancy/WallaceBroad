
wecho "
    cat ./test.tsv
    | /Users/minxian/Broad/Program/miniconda3/envs/edger/bin/Rscript
        ./GLMCovariateRegressor.R
        -c <(cat ./cov.csv | wcut -f1- -d ',')
        -f 'SCORE~TIME+GENO+iCPMsum+TIME*GENO'
        -i NAME
        --dc 3
    > test.out.tsv
"
