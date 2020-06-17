# The only different genotype: 1/1:1,3:1:3:.:.:0,3,28 and 0/0:0,0:4:6:.:.:0,6,67
# as cyvcf2 use AD field, vcftools use DP field.

wecho "
    diff <(gunzip -dc out.test.gz ) <(gunzip -dc out.test.vcftools.gz ) > compare.txt
"
