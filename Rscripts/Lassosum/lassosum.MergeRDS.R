#!/usr/bin/env Rscript

'

Merge lassosum chunk-wise(e.g. chr by chr) RDS files.
* Read RDS file list from stdin.

usage: lassosum.MergeRDS.R -o <obase>
-o <obase>    Output file name base.
' -> doc

# load the docopt library and parse options.
library(docopt)
opts <- docopt(doc)
# str(opts$s)
# str(opts)

out.prs = opts$o
# print(out.prs)
dd = read.table(file("stdin"),header = F)
print('Loaded RDS files:')
# print(as.character(dd[,1]))

library(lassosum)
library(data.table)
fl = as.character(dd[,1])
# rds = lapply(as.character(dd[,1]), "readRDS")
out = merge(readRDS(fl[1]),readRDS(fl[2]))
print(fl[1:2])
for(i in 3:length(fl)){
    out = merge(out,readRDS(fl[i]))
    print(fl[i])
}
saveRDS(out,file=paste(out.prs,'.rds',sep=""))
