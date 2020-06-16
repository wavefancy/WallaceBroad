
gunzip -dc ../VCFDPFilter/test.maf0.3.vcf.gz | python3 ./VCFHETMinorReadsRatioFilter.py -c 0.4 | bgzip > out.test.vcf.gz
