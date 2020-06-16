
cat ../VCFDPFilter/test.vcf | python3 ./VCFHOMOMinorReadsRatioFilter.py -c 0.1 | bgzip > out.test.vcf.gz
