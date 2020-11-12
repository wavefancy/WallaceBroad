'
Rare variant burden/collapse test based on SPATest/Firth logistic regression for binary pheno
or by a multiple regression for continuous trait (glm). SPA is a score test method corrected for
(qusi)-separation and inbalance case/control ratio. The overalll performance is very close to
Firth biased-corrected method, but with about 100x faster than Firth method.

Ref: A Fast and Accurate Algorithm to Test for Binary Phenotypes and Its Application to PheWAS

Notes:
  * Read gene level score from stdin and output results to stdout.
  * The output SPA P value has been signed, for indicating the effect direction.
  * For the SPA test, we use fastSPA=2, minmac = 1.
  * This load all version is 3x faster than read line by line.

Usage:
  RareRegressionAuto.R -f file -p pheno -i id [-c covariates] [--dc int] [--firthP float]

Options:
  -f file         Covariates file (including ID, Phenotype and covariates).
                     TSV with header, missing coded as NA.
  -p pheno        Phenotype name.
  -i id           Column name for individual id.
  -c covariates   Specifiy covariates, eg.: cov1,cov2|cov1.
  --dc int        From which column the individual score data starts [8], index start from 1.
  --firthP float  The P value cut-off from SPA to call the firth logistic regression 
                      for estimating beta and beta_se, [1.0].
  ' -> doc

# load the docopt library and parse options.
suppressPackageStartupMessages(library(docopt))
suppressPackageStartupMessages(library(stringi))
suppressPackageStartupMessages(library(SPAtest))
opts <- docopt(doc)

# str(opts)

pedfile = ifelse(is.null(opts$f)==F, opts$f, NULL)
pheno   = ifelse(is.null(opts$p)==F, opts$p, NULL)
idname  = ifelse(is.null(opts$i)==F, opts$i, NULL)
covnames= ifelse(is.null(opts$c)==F, opts$c, NULL)
datacol = if(is.null(opts$dc)) 8 else as.numeric(opts$dc)
firthP  = if(is.null(opts$firthP)) 1.0 else as.numeric(opts$firthP)

mf = function(x){if(is.na(x)) 'NA' else formatC(x, digits = 4, format = "E")}
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
tfile = OpenRead(pedfile)
# **** IMPORTANT: read.table will auto ignore comment lines.
# sep as white spaces: more spaces, tabs, newlines or carriage returns.
# set comment char as %, do not ignore # as comment.
ped = read.table(tfile, header=T, comment.char = "%")
close(tfile)
# load data from stdin line by line,
# do the test gene by gene.
input <- file('stdin', 'r')
myhead <- stri_split_regex( readLines(input, n=1), "\\s+" )[[1]]

# Prepare the covariates, or just the intercept.
COVS = ifelse( is.null(covnames) == F, stri_replace_all_fixed(covnames,",","+"), "1")

# Match the common samples, then we will extract by index, so only need match by once.
common_id_index = match(ped[[idname]],myhead)
# common_id_index
# Subset to the common samples we will do the test.
ped = ped[is.na(common_id_index)==F,]
common_id_index = common_id_index[is.na(common_id_index)==F]
# common_id_index

# Check pheno as binary or continuous.
n_pheno = dim(unique(ped[pheno]))[1]
binaryPheno = if(n_pheno==2) T else F
# dim(unique(ped[pheno]))
if(binaryPheno){
    MSGE("Two unique values detected for phenotype: %s, assume binary phenotype, use SPA.\n", pheno)
}else{
    MSGE("More than two unique values detected for phenotype: %s, assume continuous, use glm.\n", pheno)
    # No covariate, set as empty.
    if(COVS=='1'){COVS=''}
}
fm = paste0(c(pheno,'~score+',COVS),collapse='')
MSGE('Regression formula: %s\n',fm)

outtitle = T
COVS = stri_split_fixed(COVS,'+')[[1]]
for (line in readLines(input)){
    line
    ss = stri_split_regex( line, "\\s+" )[[1]]
    if(outtitle==T){ #output title line
        if(binaryPheno){
            out = c(myhead[1:datacol], c("NS", "FRAC_WITH_RARE", "SPA_PVALUE", "BETA", "SEBETA","WALD_PVALUE","SPLDATA"))
        }else{
            out = c(myhead[1:datacol], c("NS", "FRAC_WITH_RARE", "PVALUE", "BETA", "SEBETA","TVALUE"))
        }
        cat(out,sep="\t")
        cat("\n")
        outtitle=F
    }
    # print(common_id_index)
    # print(ss)
    
    genos = as.numeric(ss[common_id_index])
    rare_count = length(which(genos>0))

    out = c(ss[1:datacol], length(genos), mf(rare_count*1.0/length(genos)))
    genos
    if(binaryPheno){
        # SPA test for binary phenotype.
        # If the number of carriers less than 3, skip the estimation.
        if (rare_count < 1){
            out = c(out, "NA", "NA", "NA", "NA", "NA")
        }else{
            if (is.null(covnames)){
                # CALL fastSPA-2 for get the results return quickly, 
                # detail please check the AJHG paper: A Fast and Accurate Algorithm to Test for Binary Phenotypes and Its Application to PheWAS
                fit = ScoreTest_SPA_wMeta(genos,ped[pheno],minmac=1,Cutoff=2,
                          output="metaspline",beta.out=T,beta.Cutoff = firthP)
            }else{
                fit = ScoreTest_SPA_wMeta(genos,ped[pheno],ped[COVS],
                    minmac=1,Cutoff=2,output="metaspline",
                    beta.out=T, beta.Cutoff = firthP
                )
            }
            # Two tail P value.
            # https://www.statology.org/p-value-of-z-score-r/
            pv = 2*pnorm(q=abs(fit$beta/fit$SEbeta), lower.tail=FALSE)
            out = c(out, mf(fit$p.value), mf(fit$beta), mf(fit$SEbeta), mf(pv), paste0(fit$spldata,collapse = ','))
        }
    }else{
        # Continuous phenotype use glm instead.
        ped[['score']] = genos
        g = glm(as.formula(fm),data = ped, family = 'gaussian')
        r = coef(summary(g))
        # print(coef(summary(g)))
        # print(r['score',1])
        beta = r['score',1]
        beta_se = r['score',2]
        t = r['score',3]
        p = r['score',4]
        out = c(out, mf(p), mf(beta), mf(beta_se), mf(t))
    }
    
    cat(out,sep="\t")
    cat("\n")
}
close(input)
