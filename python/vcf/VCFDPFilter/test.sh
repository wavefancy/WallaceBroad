
wecho "
    cat test.vcf | python3 ./VCFDPFilter.py --mindp 3 --maxdp 20 | gzip >out.test.gz
    !!
    cat test.vcf | vcftools --vcf - -c --recode --minDP 3 --maxDP 20 | gzip > out.test.vcftools.gz
"

