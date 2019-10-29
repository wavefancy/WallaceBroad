### Conda installation guide for SAIGE

SAIGE is an association test software, which supports single-variant association tests, gene-based tests (SKAT-O, SKAT, BURDEN), as well as conditional analysis based on summary statistics for both single variant and gene-based tests.
More from [here](https://github.com/weizhouUMICH/SAIGE/wiki/Genetic-association-tests-using-SAIGE).

#### Receipt for installation by conda

```
# Create a conda environment `RSAIGE8` 
conda create -n RSAIGE8 r-essentials r-base=3.6.1 python=2.7
conda install -c anaconda cmake
conda install -c conda-forge gettext lapack r-matrix
conda install -c r r-rcpp  r-rcpparmadillo r-data.table r-bh
conda install -c conda-forge r-spatest r-rcppeigen r-devtools  r-skat
conda install -c bioconda r-rcppparallel r-optparse
conda install -c anaconda boost zlib
pip install cget click

# Using method 3
conda activate RSAIGE8
# Open R and install package MetaSKAT
> install.packages('MetaSKAT')
# exit R and run bellow command
src_branch=master
repo_src_url=https://github.com/weizhouUMICH/SAIGE
git clone --depth 1 -b $src_branch $repo_src_url
R CMD INSTALL SAIGE

# Using by method 2
conda activate RSAIGE8
# open R and run (choose 3 no update any packages): 
devtools::install_github("weizhouUMICH/SAIGE") 
```

#### Restore from the receipt I have created.
- Download the `RSAIGE8.yml` in this repository
- Restore the virtual environment, and install by `devtools`

```
conda env create -n RSAIGE9 -f RSAIGE8.yml
conda activate RSAIGE9
# open R and run (choose 3 no update any packages): 
devtools::install_github("weizhouUMICH/SAIGE") 
```
