# Get the small vcf
#  cat ../VCFDPFilter/test.vcf | head -n 211 | wcut -f1-13 --cs '##' -c  > small.vcf

 cat ./small.vcf | python3 ./VCF_AD_DP_MissingByGQ.py --minGQ 3 > out.test.txt
