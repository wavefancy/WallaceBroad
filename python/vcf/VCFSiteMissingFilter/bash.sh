# Filter by missingrate <= 0.3
wecho "
    cat ../VCFDPFilter/test.vcf | python3 ./VCFSiteMissingFilter.py -m 0.1 | bgzip > miss01.vcf.gz
    !!cat ../VCFDPFilter/test.vcf | wc -l
    !!gunzip -dc miss01.vcf.gz | wc -l
    !!gunzip -dc miss01.vcf.gz | vcftools --vcf - -c --missing-site | bgzip > sites.missing01.txt.gz
    !!cat ../VCFDPFilter/test.vcf | vcftools --vcf - -c --missing-site | bgzip > sites.missing.txt.gz
"
