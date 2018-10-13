'
Compute PRS score by lassosum, validation and output the beta and PRS for the best validation.
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
RegularizeFactor = opts$r
summary_sample_size = as.integer(opts$n)
summary=opts$s

# ------------------------
# ncpu=3
# out.prs="test"
# test.bfile="data/validate.all"
# ref.bfile="data/validate.all"
# RegularizeFactor=1
# summary_sample_size=235705
# summary="data/summary.all.txt"
# ------------------------

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
cor <- p2cor(p = ss$p, n = summary_sample_size, sign=log(ss$or))
# n is the sample size

#only fork if we need more than one threads.
if (ncpu==1){
  out <- lassosum.pipeline(cor=cor, chr=ss$hg19chrc, pos=ss$bp,
              A1=ss$a1, A2=ss$a2,
              ref.bfile=ref.bfile, test.bfile=test.bfile,
              # ref.bfile=ref.bfile,
              s = c(as.numeric(RegularizeFactor)),
             LDblocks = ld)
}else{
  library(parallel)
  cl <- makeCluster(ncpu, type="FORK")
  out <- lassosum.pipeline(cor=cor, chr=ss$hg19chrc, pos=ss$bp,
              A1=ss$a1, A2=ss$a2,
              ref.bfile=ref.bfile, test.bfile=test.bfile,
              # ref.bfile=ref.bfile,
              s = c(as.numeric(RegularizeFactor)),
             LDblocks = ld, cluster=cl)
}
# Do not do validation here, just output the lassosum coefficient scores.

vls <- validate(out)
print(c('best.validation.result:',vls$best.validation.result))
print(c('validation.type:',vls$validation.type))

y = out$beta[[RegularizeFactor]]
r = cbind(ss[out$also.in.refpanel,]$snpid, ss[out$also.in.refpanel,]$a1, ss[out$also.in.refpanel,]$a2,summary(vls$best.beta))
m = c('snpid','a1','a2','beta')
colnames(r)=m
write.table(r,file=paste(out.prs,'_rebeta_',RegularizeFactor,'.txt',sep=""),col.names=T,row.names=F,quote=F)
write.table(vls$results.table,file=paste(out.prs,'_validation_',RegularizeFactor,'.txt',sep=""),col.names=T,row.names=F,quote=F)
# only use one threads.
# library(parallel)
# cl <- makeCluster(ncpu, type="FORK")
