#!/usr/bin/env Rscript

'
Run lassosum chr by chr, save rds files.

*** The default LDblocks information was set as European ancestry.
*** Input file should have these columns: "CHR     BP      A1      A2      OR      P    SNP"

usage: lassosum.CHR2RDS.R -s <sfile> -n <int> -t <tfile> -o <obase> [-c <int>] [-l <lfile>]
options:
-s <sfile>    Summary statistics files
-n <int>      The sample size for the summary statistics.
-t <tfile>    Test plink file, validation individuals.
-l <lfile>    LD reference file, if not set, the same as -t, test file.
-o <obase>    Output file name base.
-c <int>      Number of cpus for computing, default 1.
' -> doc

# load the docopt library and parse options.
library(docopt)
opts <- docopt(doc)
# str(opts$s)
# str(opts)

# 10K individuals 10G memory.
# The number of cpus, default as 1
ncpu=1
if (is.null(opts$c)==F){
  ncpu = as.integer(opts$c)
}
ref.bfile = NULL
if (is.null(opts$l)==F){
  ref.bfile = opts$l
}
# out.prs <- paste(dir,"lassosum",sep="")
out.prs = opts$o
test.bfile = NULL
if (is.null(opts$t)==F){
  test.bfile = opts$t
}
summary_sample_size = as.integer(opts$n)
summary=opts$s

#ncpu=3
#out.prs="test"
#test.bfile="data/validate.all"
#ref.bfile="data/validate.all"
#RegularizeFactor=0.2
#summary_sample_size=235705
#summary="data/summary.all.txt"

#dump all variable until now.
# dump(ls(pattern = '.'), "")
# q()

### Read ld region file ###
#setwd(system.file("data", package="lassosum"))
library(lassosum)
library(data.table)
#summary
# ss <- fread(paste(dir,"summary.all.txt",sep=""))
# ss <- fread(opts$s)
ss <- fread(summary)
#ld <- fread("/medpop/esp2/wallace/tools/lassosum/lassosum/inst/data/Berisa.EUR.hg19.bed")
#use the ld block from the data packages.
ld="EUR.hg19"
cor <- p2cor(p = ss$P, n = summary_sample_size, sign=log(ss$OR))
# n is the sample size

#only fork if we need more than one threads.
if (ncpu==1){
  out <- lassosum.pipeline(cor=cor, chr=ss$CHR, pos=ss$BP,
              A1=ss$A1, A2=ss$A2,snp=ss$SNP,
              ref.bfile=ref.bfile, test.bfile=test.bfile,
              # ref.bfile=ref.bfile,
              # s = c(as.numeric(RegularizeFactor)),
             trace=2,
             LDblocks = ld)
}else{
  library(parallel)
  cl <- makeCluster(ncpu, type="FORK")
  out <- lassosum.pipeline(cor=cor, chr=ss$CHR, pos=ss$BP,
              A1=ss$A1, A2=ss$A2,snp=ss$SNP,
              ref.bfile=ref.bfile, test.bfile=test.bfile,
              # ref.bfile=ref.bfile,
              # s = c(as.numeric(RegularizeFactor)),
             trace=2,
             LDblocks = ld, cluster=cl)
}

saveRDS(out, file=paste(out.prs,'.rds',sep=""))
# Do not do validation here, just output the lassosum coefficient scores.
# y = out$beta[[RegularizeFactor]]
# x = apply(y,2,"sum")
# t = y[,x!=0]
# r = cbind(ss[out$also.in.refpanel,]$snpid, ss[out$also.in.refpanel,]$a1, ss[out$also.in.refpanel,]$a2,t)
# n = paste('beta',seq(1,dim(t)[2]),sep='')
# m = c(c('snpid','a1','a2'),n)
# colnames(r)=m
# write.table(r,file=paste(out.prs,'_rebeta_',RegularizeFactor,'.txt',sep=""),col.names=T,row.names=F,quote=F)
# only use one threads.
# library(parallel)
# cl <- makeCluster(ncpu, type="FORK")

### Validation with phenotype ###
#v <- validate.lassosum.pipeline(out) # Use the 6th column in .fam file in test dataset for test phenotype
# In newer version, structure changed from: validate.lassosum.pipeline to validate
#v <- validate(out) # Use the 6th column in .fam file in test dataset for test phenotype
#write.table(v$pgs[RegularizeFactor],file=paste(out.prs,'rs_',RegularizeFactor,'.txt',sep=""),col.names=F,row.names=F)
# write.table(v$pgs$"0.5",file=paste(out.prs,'.d0.5.txt',sep=""),col.names=F,row.names=F)
# write.table(v$pgs$"0.9",file=paste(out.prs,'.d0.9.txt',sep=""),col.names=F,row.names=F)
# write.table(v$pgs$"1",file=paste(out.prs,'.d1.0.txt',sep=""),col.names=F,row.names=F)
#write.table(v$best.pgs,file=paste(out.prs,'rs_',RegularizeFactor,'.best.pgs.txt',sep=""),col.names=F,row.names=F)
