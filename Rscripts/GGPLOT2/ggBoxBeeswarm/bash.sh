
wecho "
    gunzip -dc toothgrowth.csv.gz
        | Rscript ./ggHalves.R -x dose -y len
        -c supp
        -o test.pdf -W  5 -H 3
        --xo '2::0.5::1' --wl 3
"
