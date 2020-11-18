
wecho "
    gzip -dc ../VCFCountScore4GeneMask/hg19.gene.ANGPTL8.vcf.gz | VCFSetID.py > temp.vcf
    &&
    plink2
        --vcf temp.vcf
        --make-pgen
        --out hg19.gene.ANGPTL8
    &&
    rm temp.vcf
"
wecho "
    cat ./test.indels.missing.vcf | VCFSetID.py > temp.vcf
    &&
    plink2
        --vcf temp.vcf
        --make-pgen
        --vcf-half-call m
        --out test.indels.missing
    &&
        rm temp.vcf
"
