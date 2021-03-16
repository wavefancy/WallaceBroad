'
Adjust the GWAS variant weight by LDpred2 algorithm.

Notes:
  * The GWAS summary must has the following columns:
        chr, pos, rsid, a1, a0, beta, beta_se, n_eff
  * The rsid is snpid, can be any unique text.
  * The LD reference panel were stored in separated chr, plink 1.0 bed/bim/fam format.

Usage:
  LDpred2.R -o prefix -g gwas -p bfile

Options:
  -o prefix     Output file name prefix.
  -g gwas       GWAS summary statisic file.
  -p bfile      Plink bed/fam/bim file name template for LD reference, split by each chr.
                    eg. eur.ref.chr#.ref -> will be interpreted as: 
                        eur.ref.chr1.ref, eur.ref.chr2.ref ... eur.ref.chr22.ref
' -> doc

# Pipeline for running LDpred2.
# https://choishingwan.github.io/PRS-Tutorial/ldpred/
# https://privefl.github.io/bigsnpr/articles/LDpred2.html

# conda install 

suppressMessages(library(dplyr))
suppressMessages(library(docopt))
suppressMessages(library(rio))
suppressMessages(library(data.table))
suppressMessages(library(magrittr))

opts <- docopt(doc)
# what are the options? Note that stripped versions of the parameters are added to the returned list
# str(opts)
gfile  = opts$g
pref   = opts$p %>% strsplit(.,'#') %>% unlist
outp   = opts$o
MSGE <- function(...) cat(sprintf(...), sep='', file=stderr())

# END parse parameter

# On some server, you might need to first use the following code in order to run LDpred with multi-thread
suppressMessages(library(bigsnpr))
options(bigstatsr.check.parallel.blas = FALSE)
options(default.nproc.blas = NULL)

sumstats <- bigreadr::fread2(gfile)

# ***** Calculate the LD matrix *****
# Get maximum amount of cores, +1 to use all available cpus.
NCORES <- nb_cores()+1
# Open a temporary file
tmp <- tempfile(tmpdir = "tmp-data")
on.exit(file.remove(paste0(tmp, ".sbk")), add = TRUE)

# Initialize variables for storing the LD score and LD matrix
corr <- NULL
ld <- NULL
# We want to know the ordering of samples in the bed file 
info_snp <- NULL
fam.order <- NULL
for (chr in 1:22) {
    # preprocess the bed file (only need to do once for each data set)
    # Assuming the file naming is eur.ref.chr#.ref
    bed_file = paste0(pref[1],chr,pref[2],"bed")
    if(file.exists(bed_file) == FALSE){
        MSGE('WARN: no LD reference for chr: %d, no file found:%s \n',chr, bed_file)
        next
    }
    cat(sprintf('-------WORKING CHR: %d-------',chr))
    # If the object has been created, we just need re-attach, no not need recreate.
    # The snp_readBed will create the rds and bk files.
    # https://privefl.github.io/bigsnpr/reference/snp_readBed.html
    if(file.exists(paste0(pref[1],chr,pref[2],"rds")) == FALSE){
        # snp_readBed(bed_file, ncores = NCORES)
        snp_readBed(bed_file)
    }
    # now attach the genotype object
    obj.bigSNP <- snp_attach(paste0(pref[1],chr,pref[2],"rds"))
    # extract the SNP information from the genotype
    map <- obj.bigSNP$map[-3]
    names(map) <- c("chr", "rsid", "pos", "a1", "a0")
    # perform SNP matching
    tmp_snp <- snp_match(sumstats[sumstats$chr==chr,], map)
    info_snp <- rbind(info_snp, tmp_snp)
    # Assign the genotype to a variable for easier downstream analysis
    genotype <- obj.bigSNP$genotypes
    # Rename the data structures
    CHR <- map$chr
    POS <- map$pos
    # get the CM information from 1000 Genome
    # will download the 1000G file to the current directory (".")
    POS2 <- snp_asGeneticPos(CHR, POS, dir = ".")
    # calculate LD
    # Extract SNPs that are included in the chromosome
    ind.chr <- which(tmp_snp$chr == chr)
    ind.chr2 <- tmp_snp$`_NUM_ID_`[ind.chr]
    # Calculate the LD
    corr0 <- snp_cor(
            genotype,
            ind.col = ind.chr2,
            ncores = NCORES,
            infos.pos = POS2[ind.chr2],
            size = 3 / 1000
        )
    if (chr == 1) {
        ld <- Matrix::colSums(corr0^2)
        corr <- as_SFBM(corr0, tmp)
    } else {
        ld <- c(ld, Matrix::colSums(corr0^2))
        corr$add_columns(corr0, nrow(corr))
    }
    # We assume the fam order is the same across different chromosomes
    if(is.null(fam.order)){
        fam.order <- as.data.table(obj.bigSNP$fam)
    }
}
# Rename fam order
setnames(fam.order,
        c("family.ID", "sample.ID"),
        c("FID", "IID"))

# Perform LD score regression
df_beta <- info_snp[,c("beta", "beta_se", "n_eff", "_NUM_ID_")]
ldsc <- snp_ldsc(   ld, 
                    length(ld), 
                    chi2 = (df_beta$beta / df_beta$beta_se)^2,
                    sample_size = df_beta$n_eff, 
                    blocks = NULL)
h2_est <- ldsc[["h2"]]

# Prepare data for grid model, using the default parameters.
p_seq  <- signif(seq_log(1e-4, 1, length.out = 17), 2)
h2_seq <- round(h2_est * c(0.7, 1, 1.4), 4)
grid.param <-
            expand.grid(p = p_seq,
            h2 = h2_seq,
            sparse = c(FALSE, TRUE))
grid.param.name <-
     expand.grid(p = paste0('p:',p_seq),
             h2 = paste0('h2:',c(0.7, 1, 1.4)),
             sparse = c('F', 'T'))
gpn = do.call("paste", c(grid.param.name, sep = "_"))

# Save the grid.param values, has the different heritability values.
export(grid.param, paste0(outp,"grid.param.values.tsv"))

# Get adjusted beta from grid model
beta_grid <-
    snp_ldpred2_grid(corr, df_beta, grid.param, ncores = NCORES)

t = as.matrix(info_snp[,c('rsid','a1','a0')],ncol=3)
out = cbind(t,beta_grid)
colnames(out) =  c(c('rsID','a1','a0'),gpn)
export(out, paste0(outp,'beta_grid.tsv.gz'),quote=F)
