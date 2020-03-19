#!/usr/bin/env Rscript

# @Wallace Wang, wavefancy@gmail.com
#------------------------------

"
=============================================================
* Partition the data into two parts, usually by PRS score, then 
compare the OR for the top to the rest of the data for estimating of the OR.

* Added a new variable as G with value as 1/0 corresponding to 
top group vs the rest. So the variable names G can be used in the formula [-f]. 

Usage:
ORTop2Rest.R -n name -p float -f string
ORTop2Rest.R -h [--help]

Options:
-n name    Variable name for partition the data.
-p float   Proportion of data in the top group, eg 0.05.
-f string  The formula for modeling the data, eg. CAD~G+PC1+PC2+age.

Notes:
1. Read data from stdin and output results to stdout.
=============================================================
" -> doc

suppressMessages(library(docopt))
suppressMessages(library(data.table))
suppressMessages(library(stringr))

opts <- docopt(doc)

##### Taking parameters ########
# variable name for partition the data.
gName  = 'PRS'
# formula string for modeling.
fsting = 'PHENO ~ G + PC1 + PC2 + PC3 + PC4 + PC5 + SEX + agevisit0'
phenoName = 'PHENO'
# The cutting point, 1-proporiton_of_people in the top group.
p = 0.9

##### Take values from arguments ########
gName = opts$n
fsting = opts$f
p = 1 - as.numeric(opts$p)
phenoName = str_trim(str_split(fsting,'~')[[1]][1])


##### Start the main function ########
#data = fread("normed.best.covs.gz")
data = read.table(file("stdin"),header = T)

f = as.formula(fsting)
fmt  = function(x){formatC(x, digits = 2, format = "f")}
fmtP = function(x){formatC(x, digits = 2, format = "e")}

# Assume the data has been partitoned in groups by gName,
# The partiton group factor names as G, factor '0' in G will be the reference group.
# This function will estimate the OR, CI, counts and P for each group 
# Compared to the ref_G group in a glm regression framework.
groupOR = function(data,f){
  # force the G0 as the reference.
  ref_G='0'
  #ref_G = '3' # reference group name.
  mydata <- within(data, G <- relevel(G, ref = ref_G))
  g = glm(f, family = 'binomial', data=mydata)
  
  #for the estimation of OR and P. 
  k = summary(g)
  k_sub = k$coefficients['G1',]
  OR = exp(k_sub['Estimate'])
  
  # for the estimation of CI for OR.
  ci = suppressMessages(confint(g))
  OUTCI = exp(ci['G1',])
  # print(OUTCI)
  # count the number of case and controls
  counts = table(mydata$G,mydata[[phenoName]])
  # print(counts)
  
  out_data = data.frame(
    GROUP = c('G0','G1'),
    OR=fmt(c(1,OR)), 
    CI95_L=fmt(c(1,OUTCI[1])), 
    CI95_R=fmt(c(1,OUTCI[2])),
    CTRL_N = counts[,'0'],
    CASE_N = counts[,'1'],
    P = fmtP(c(1,k_sub[4])))
  #     return out_data
}

# partion data according to varibale in two groups.
pcut = quantile(data[[gName]], probs =  c(0,p,1))
data[['G']] = cut(data[[gName]], breaks = pcut, labels = as.character(c(0,1)))

topOR = groupOR(data,f)
write.table(topOR,'', row.names = F, quote = F)
