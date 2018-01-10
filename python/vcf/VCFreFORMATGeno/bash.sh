
zcat test1.vcf.gz | python3 VCFreFORMATGeno.py -t PL,GT,GQ | bgzip >out.vcf.gz

