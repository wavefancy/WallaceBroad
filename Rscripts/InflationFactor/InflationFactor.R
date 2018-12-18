# Rscript ~/Rscripts/InflationFactor.R col4Pvalue
#
# Estimate InflationFactor from input pvalues.
#------------------------------
# Read data from stdin(One column for pvalue)
# Output results to stdout.
# @Wallace Wang, wavefancy@gmail.com
#------------------------------

library(GenABEL)

args <- commandArgs(TRUE)
if(length(args) != 1){
    print(args)
    print("Please set arguments: 'arg1' for the column of pvalues, 1 based.")
    quit()
}
col = as.numeric(args[1])

inData = read.table(file("stdin"))
re = estlambda(inData[,col], plot = F)
out = matrix(re, nrow =1)
colnames(out) = c('estimate','se')
write.table(out, stdout(), col.names = T, row.names = F, quote = F, sep='\t')
