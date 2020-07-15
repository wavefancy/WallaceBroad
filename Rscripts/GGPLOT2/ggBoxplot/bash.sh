
wecho "
    gunzip -dc toothgrowth.csv.gz
        | Rscript ./ggBoxplot.R -x dose -y len
        -c supp
        -o test.pdf -W  4 -H 3
        --xo '2::0.5::1' --wl 3
"
