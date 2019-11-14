
gunzip -dc test1.vcf.gz | python3 VCFSetID.py -s | bgzip >out.vcf.gz
