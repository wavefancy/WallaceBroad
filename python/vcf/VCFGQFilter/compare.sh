# Compare the results with vcftools.
wecho "
    diff <(gunzip  -dc mingq20.vcftools.vcf.gz ) <(gunzip -dc mingq20.cyvcf2.vcf.gz | grep -vi 'VCFGQFilter.py' | grep -vi 'ID=PASS' ) > ./compare.txt
"
