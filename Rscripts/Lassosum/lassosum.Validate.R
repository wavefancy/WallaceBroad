#!/usr/bin/env Rscript

'

Validate lassosum based on a new dataset.

usage: lassosum.Validate.R -t <tfile> -r <rds> -o <obase>
-r <rds>      Saved rds file.
-t <tfile>    Test bed file stem.
-o <obase>    Output file name base.
' -> doc

# load the docopt library and parse options.
library(docopt)
opts <- docopt(doc)
# str(opts$s)
# str(opts)

out.prs = opts$o
test.file = opts$t
rds = opts$r

out.prs =
test.file =
rds =

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
