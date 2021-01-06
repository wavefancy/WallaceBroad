
wecho "
    cat ./test.tsv
    | /Users/minxian/Broad/Program/miniconda3/envs/edger/bin/Rscript
        ./GLMCovariateStandardizer.R
        -c <(cat ./cov.csv | wcut -f1- -d ',')
        -f 'SCORE~GENO'
        -i NAME
        --dc 3
    > test.out.tsv
"
