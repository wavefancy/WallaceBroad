#
# Covert gene names between different annotations.
# @Wallace Wang, wavefancy@gmail.com
# --------------------------------
# Dependent packages.
# source("https://bioconductor.org/biocLite.R")
# biocLite("org.Hs.eg.db")
# source("https://bioconductor.org/biocLite.R")
# biocLite("clusterProfiler")
# install.packages('docopt')
#
#
'
=======================================================================================
Pairwise GWAS driver colocalization test.

Usage:
    coloc.R
    coloc.R -h [--help]

Options:


Notes:
    1. Read one column data from stdin.
    2. Output results to stdout.

' -> doc

# load the docopt library
library(docopt)
# retrieve the command-line arguments
opts <- docopt(doc)
# what are the options? Note that stripped versions of the parameters are added to the returned list
# str(opts)
# from = unlist(opts['from'][[1]])
# to = strsplit(opts['to'][[1]],',')
# to = c(from, unlist(to))

library(coloc)
# dd = read.table(file("stdin"),header = T)
dd = read.table("peak.1-38386727.txt",header = T)
# ids <- bitr(dd[,1], fromType="SYMBOL", toType=c("UNIPROT", "ENSEMBL","ENTREZID","GENENAME"), OrgDb="org.Hs.eg.db")
# ids <- bitr(dd[,1], fromType=from, toType=to, OrgDb="org.Hs.eg.db")

# Ref: https://github.com/chr1swallace/coloc/blob/362d0f13c94df126f2e4861f3db1b144c23d8122/tests/testthat/test-abf.R
sd.est1 <- coloc:::sdY.est(vbeta=dd[,3], maf=dd[,4], n=282420)
sd.est2 = coloc:::sdY.est(vbeta=dd[,6], maf=dd[,7], n=282420)

d1 = list(beta=dd[,2],varbeta=dd[,3],type="quant",sdY=sd.est1)
d2 = list(beta=dd[,5],varbeta=dd[,6],type="quant",sdY=sd.est2)
coloc.abf(d1,d2)

write.table(ids, stdout(), quote=F, row.names=F, col.names=T,sep='\t')
