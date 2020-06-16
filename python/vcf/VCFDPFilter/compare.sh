# The only different genotype: 1/1:1,3:1:3:.:.:0,3,28
# as cyvcf2 use AD field, vcftools use DP field.

wecho "
    diff <(gunzip -dc out.test.gz ) <(gunzip -dc out.test.vcftools.gz ) > compare.txt
"
