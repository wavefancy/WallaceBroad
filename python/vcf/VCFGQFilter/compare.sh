# Compare the results with vcftools.
wecho "
    diff <(gunzip  -dc mingq20.vcftools.vcf.gz ) <(gunzip -dc mingq20.cyvcf2.vcf.gz ) > ./compare.txt
"
