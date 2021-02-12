wecho "
    echo -e 'ENSMUSG00000102693\nENSMUSG00000064842'
    |  /Users/minxian/Broad/Program/miniconda3/envs/decompose/bin/Rscript
        GenenameConverter.Mouse.R -f ENSEMBL -t SYMBOL
    > ./results.mouse.txt
"
