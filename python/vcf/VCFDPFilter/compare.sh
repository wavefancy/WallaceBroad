# In compare one.
# The only different genotype: 1/1:1,3:1:3:.:.:0,3,28 and 0/0:0,0:4:6:.:.:0,6,67
# as cyvcf2 use AD field, vcftools use DP field.

# In compare two.
# For complete sites. vcftools will reset the missing genotype.
# At: 1     17454   .       T       C
# VCFDPFilter.py: .:.:.:.:.
# vcftools: ./.:.:.:.:.

wecho "
      diff <(gunzip -dc out.test.gz ) <(gunzip -dc out.test.vcftools.gz ) > out.compare.txt
    !!diff <(cat test.vcf | python3 ./VCFDPFilter.py --mindp 3 --maxdp 20 --field DP) <(gunzip -dc out.test.vcftools.gz ) > out.compare.2.txt
"
