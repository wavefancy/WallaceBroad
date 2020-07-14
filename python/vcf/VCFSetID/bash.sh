
gunzip -dc test1.vcf.gz | python3 VCFSetID.py -s -m 15 | bgzip >out.vcf.gz
