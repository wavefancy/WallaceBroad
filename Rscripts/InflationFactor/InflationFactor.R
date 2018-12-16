# Rscript ~/Rscripts/InflationFactor.R col4Pvalue
#
# Estimate InflationFactor from input pvalues.
# **** Please only streem in numerical data, no string ***
#------------------------------
# Read data from stdin(One column for pvalue)
# Output results to stdout.
# @Wallace Wang, wavefancy@gmail.com
#------------------------------
# Methods from:
# https://stats.stackexchange.com/questions/110755/calculate-inflation-observed-and-expected-p-values-from-uniform-distribution-in

#library(GenABEL)

args <- commandArgs(TRUE)
if(length(args) != 1){
    print(args)
    print("Please set arguments: 'arg1' for the column of pvalues, 1 based.")
    quit()
}
col = as.numeric(args[1])

inData = read.table(file("stdin"))
pvalue = inData[,col]
chisq <- qchisq(1-pvalue,1)
lambda = median(chisq)/qchisq(0.5,1)

#re = estlambda(inData[,col], plot = F)
#out = matrix(re, nrow =1)
#colnames(out) = c('estimate','se')
write.table(lambda, stdout(), col.names = F, row.names = F, quote = F, sep='\t')
