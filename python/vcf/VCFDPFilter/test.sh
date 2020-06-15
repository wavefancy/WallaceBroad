
wecho "
    cat test.vcf | python3 ./VCFDPFilter.py --mindp 3 --maxdp 100 | gzip >out.test.gz
"

