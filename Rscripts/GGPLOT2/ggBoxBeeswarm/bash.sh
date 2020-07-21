
# Each group has multiple group of values.
wecho "
    gunzip -dc toothgrowth.csv.gz
        | Rscript ./ggBoxBeeswarm.R -x dose -y len
        -c supp
        -o test.pdf -W  5 -H 3
        --xo '2::0.5::1' --wl 3
"
# Each group has only one class of values.
wecho "
    gunzip -dc toothgrowth.csv.gz
        | Rscript ./ggBoxBeeswarm.R -x dose -y len
        -c dose
        -o test2.pdf -W  5 -H 3
        --xo '2::0.5::1' --wl 3
"
