parallel -j 1 -q wecho "
    /Users/minxian/Broad/Program/miniconda3/envs/decompose/bin/Rscript ./ClusterProfilerEnrich{1}.R
    -t ./top.txt
    -b ./background.txt
    -o test.{1}
    -p 0.001
" ::: GO KEGG
