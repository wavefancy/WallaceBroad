
zcat test1.vcf.gz | python3 VCFAlleleCountsFre.py |bgzip >out.gz

gzcat test.gp.vcf.gz | python3 VCFAlleleCountsFre.py -c GP_GENO
