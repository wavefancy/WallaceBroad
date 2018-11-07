#!/usr/bin/env Rscript

'

Check out the parameter for getting the best performance.
Output results to stdout.

usage: lassosum.GetBestPara.R -f <file>
-f <file>    Input RDS files.
' -> doc

# load the docopt library and parse options.
library(docopt)
opts <- docopt(doc)
# str(opts$s)
# str(opts)

inrds = opts$f

library(lassosum)
inf = readRDS(inrds)
print(c('best.s',inf$best.s),quote=F)
print(c('best.lambda',inf$best.lambda),quote=F)
