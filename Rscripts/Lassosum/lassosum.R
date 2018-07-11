'
Compute PRS score by lassosum.
** The default LDblocks information was set as European ancestry.

usage: lassosum.R -s <sfile> -n <int> -t <tfile> -r <float> -o <obase> [-c <int>] [-l <lfile>]
options:
-s <sfile>    Summary statistics files
-n <int>      The sample size for the summary statistics.
-t <tfile>    Test plink file, validation individuals.
-l <lfile>    LD reference file, if not set, the same as -t, test file.
-r <float>    Regularize factor, one of 0.2|0.5|0.9|1, suggested by lassosum.
-o <obase>    Output file name base.
-c <int>      Number of cpus for computing, default 1.
' -> doc

# 10K individuals, 2k LD ref, 3CPUs, 30G memory.

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
# print(ncpu)
# q()
# dir="data/"
#ref ld file
# ref.bfile <- paste(dir,"validate.all",sep="")
ref.bfile = opts$t
if (is.null(opts$l)==F){
  ref.bfile = opts$l
}
# out.prs <- paste(dir,"lassosum",sep="")
out.prs = opts$o
#test file
# test.bfile <- "data/validate.all"
test.bfile = opts$t
RegularizeFactor = opts$r
summary_sample_size = as.integer(opts$n)

#dump all variable until now.
# dump(ls(pattern = '.'), "")
# q()

### Read ld region file ###
#setwd(system.file("data", package="lassosum"))
library(lassosum)
library(data.table)
#summary
# ss <- fread(paste(dir,"summary.all.txt",sep=""))
ss <- fread(opts$s)

ld <- fread("/medpop/esp2/wallace/tools/lassosum/lassosum/inst/data/Berisa.EUR.hg19.bed")
cor <- p2cor(p = ss$p, n = summary_sample_size, sign=log(ss$or))
# n is the sample size

#only fork if we need more than one threads.
if (ncpu==1){
  out <- lassosum.pipeline(cor=cor, chr=ss$hg19chrc, pos=ss$bp,
              A1=ss$a1, A2=ss$a2,
              ref.bfile=ref.bfile, test.bfile=test.bfile,
              s = c(as.numeric(RegularizeFactor)),
             LDblocks = ld)
}else{
  library(parallel)
  cl <- makeCluster(ncpu, type="FORK")
  out <- lassosum.pipeline(cor=cor, chr=ss$hg19chrc, pos=ss$bp,
              A1=ss$a1, A2=ss$a2,
              ref.bfile=ref.bfile, test.bfile=test.bfile,
              s = c(as.numeric(RegularizeFactor)),
             LDblocks = ld, cluster=cl)
}
# only use one threads.
# library(parallel)
# cl <- makeCluster(ncpu, type="FORK")

### Validation with phenotype ###
v <- validate.lassosum.pipeline(out) # Use the 6th column in .fam file in test dataset for test phenotype
write.table(v$pgs[RegularizeFactor],file=paste(out.prs,'rs_',RegularizeFactor,'.txt',sep=""),col.names=F,row.names=F)
# write.table(v$pgs$"0.5",file=paste(out.prs,'.d0.5.txt',sep=""),col.names=F,row.names=F)
# write.table(v$pgs$"0.9",file=paste(out.prs,'.d0.9.txt',sep=""),col.names=F,row.names=F)
# write.table(v$pgs$"1",file=paste(out.prs,'.d1.0.txt',sep=""),col.names=F,row.names=F)
write.table(v$best.pgs,file=paste(out.prs,'rs_',RegularizeFactor,'.best.pgs.txt',sep=""),col.names=F,row.names=F)
