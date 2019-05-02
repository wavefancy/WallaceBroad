
# zcat test1.vcf.gz | python3 VCFAlleleCountsFre.py |bgzip >out.gz
gzcat test1.vcf.gz | python3 VCFAlleleCountsFre.py -c GT_GENO | bgzip >GT.COUNTs.gz

#gzcat test.gp.vcf.gz | python3 VCFAlleleCountsFre.py -c GP_GENO
