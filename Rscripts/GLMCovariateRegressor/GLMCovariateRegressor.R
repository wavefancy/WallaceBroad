'
Combine a score file with a covariate file and then run a regression on the combined data set.
The combined data set is the covariate file added an extra column named as `SCORE`.
The score file usually list many entries (gene) for each individual (row as score, col as individual). 
The covariate file stored the covariates for each individual (row as individual, col as covariate).
The regression was run by the R glm framework, analysis formula specified by user.

Notes:
  * Read the score file from stdin and output results to stdout.
  * The combined data set

Usage:
  GLMCovariateRegressor.R -c file -f formula -i id [--dc int] [--gf family]

Options:
  -c file         Covariates file (including ID covariates).
                     TSV with header, missing coded as NA.
  -f formula      Regression formula.
  -i id           Column name for individual id, for matching two data sets.
  --dc int        From which column the individual score data starts [2], index start from 1.
  --gf family     GLM family [gaussian]. https://www.statmethods.net/advstats/glm.html
  ' -> doc

# load the docopt library and parse options.
suppressPackageStartupMessages(library(docopt))
suppressPackageStartupMessages(library(stringi))
suppressPackageStartupMessages(library(tidyverse))
opts <- docopt(doc)

# str(opts)

covfile    = opts$c
iformula   = opts$f
# deal with interaction term by * and unique
cols       = iformula %>% stri_split_regex(.,pattern='[~+*]') %>% unlist %>% str_trim %>% unique(.)
idname     = opts$i
glmfamily  = if(is.null(opts$gf)) 'gaussian' else opts$gf

datacol  = if(is.null(opts$dc)) 2 else as.numeric(opts$dc)
# shift 1 left to set as the end postion (inclusive) to copy to the stdout.
datacol  = datacol-1

# format function.
# mf = function(x){if(length(x)==1 && is.na(x)) 'NA' else formatC(x, digits = 4, format = "E")}
mf = function(x){if(length(x)==1 && is.na(x)) 'NA' else sprintf('%g', x)}
# message to stderr.
MSGE <- function(...) cat(sprintf(...), sep='', file=stderr())
# v("name: %s  age: %d\n", name, age)
# https://stackoverflow.com/questions/15784373/process-substitution
# A method to help read process substitution.
OpenRead <- function(arg) {
   if (arg %in% c("-", "/dev/stdin")) {
      file("stdin", open = "r")
   } else if (grepl("^/dev/fd/", arg)) {
      fifo(arg, open = "r")
   } else {
      file(arg, open = "r")
   }
}
cfile = OpenRead(covfile)
# **** IMPORTANT: read.table will auto ignore comment lines.
# sep as white spaces: more spaces, tabs, newlines or carriage returns.
# set comment char as %, do not ignore # as comment.
ped = read.table(cfile, header=T, comment.char = "%")
# print(ped)
close(cfile)
# load data from stdin line by line,
# do the test gene by gene.
input <- file('stdin', 'r')
myhead <- stri_split_regex(readLines(input, n=1), "\\s+" )[[1]]

# Match the common samples, then we will extract by index, so only need match by once.
common_id_index = match(ped[[idname]],myhead)
# common_id_index
# Subset to the common samples we will do the test for the data in ped file.
ped = ped[is.na(common_id_index)==F,]
common_id_index = common_id_index[is.na(common_id_index)==F]
# common_id_index

outtitle = T
#COVS = stri_split_fixed(COVS,'+')[[1]]
for (line in readLines(input)){
    # line
    ss = stri_split_regex( line, "\\s+" )[[1]]
    # print(common_id_index)
    # print(ss)
    
    genos = as.numeric(ss[common_id_index])
   
    # Continuous phenotype use glm instead.
    ped[['SCORE']] = genos

    # subset to the column we will run the regression and remove NA.
    ped = ped[,cols] %>% na.omit(.)
    # print(ped)
    # print(glmfamily)
    g = glm(as.formula(iformula),data = ped, family = glmfamily)
    # skip the intercept.
    r  = coef(summary(g)) %>% tail(.,n=-1)
    rn = rownames(r)
    # print(r)
    # print(rownames(r))

    if(outtitle==T){ #output title line
        h = rbind(paste(rn,'_BETA',sep=''), paste(rn,'_BETA.SE',sep=''), paste(rn,'_PVALUE',sep='')) %>% as.vector(.)
        out = c(myhead[1:datacol], h)
        cat(out,sep="\t")
        cat("\n")
        outtitle=F
    }

    # output the results
    out     = ss[1:datacol]
    # print(out)
    beta    = r[,1]
    beta_se = r[,2]
    pvalue  = r[,4]
    h = rbind(beta, beta_se, pvalue) %>% as.vector(.) %>% mf(.)
    out = c(out, h)

    cat(out,sep="\t")
    cat("\n")
}
close(input)
