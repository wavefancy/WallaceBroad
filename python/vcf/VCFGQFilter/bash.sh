
wecho "
    cat ../VCFDPFilter/test.vcf | python3 ./VCFGQFilter.py --mingq 20
    | bgzip > mingq20.cyvcf2.vcf.gz
    !!
    cat ../VCFDPFilter/test.vcf | vcftools --vcf - --recode -c --minGQ 20 | bgzip >mingq20.vcftools.vcf.gz
"
