# PRS based on true beta.
# Let X is matrix, nxm, n is the number of samples, m is the number of snps, n>m.
# In a chr block, we have a multi-linear regression Xb = Y.
# LSQ solution for this: b = (X'X)^-1X'Y.
# Define PRS = P = Xb = X(X'X)^-1X'Y = X(X'X)^-1(n'beta) = X*D^-1*Diag(D)*beta, D = X'X.
# beta = [b1, b2, ... bn] is the univariant regression coefficient.
# bi = (Xi'Xi)^-1XiY = XiY/n*var(X). var(X) = 1, if X normalized, n is the sample size.

# test this PRS defination by taking Y, X and beta(marginal).

doc = """A new model for generating PRS scores.

Usage:
  Cal.PRS.proto.jl [--outbeta] [--outprs] [--onlyprs] -b beta -x genomatrix -o out
  Cal.PRS.proto.jl -h | --help | --version

Options:
  --outbeta     Output adjusted beta values.
  --outprs      Output prs values after adjusting beta.
  --onlyprs     Only calculate prs based on beta and geno, no beta adjustment.
  -o out        Output prefix
  -b beta       The beta from univariant|adjusted beta analysis.
  -x genomatrix Input genotype matrix, as 0|1|2 format.
  -h --help     Show this screen.
  --version     Show version.
"""

using DelimitedFiles
# using StatsBase
using Statistics
using LinearAlgebra
using DocOpt

args = docopt(doc, version=v"0.0.0")
println(args)
# println(args["-b"])
OUT_BETA    = args["--outbeta"] ? true : false
OUT_PRS     = args["--outprs"]  ? true : false
ONLY_PRS    = args["--onlyprs"] ? true : false
UNI_BETA    = args["-b"] # univariant beta
GENO_M      = args["-x"] # genotyping matrx, sample by genotype.
OUT_PREFIX  = args["-o"] # output prefix.

# println(OUT_BETA)
# exit(0)

# X is sample*snp matrix. each row is a sample, col is a snp.
GENO_M = "x-00.txt"
X = readdlm(GENO_M,',',Float64,'\n')

# replace NaN missing as mean.
# impute row missing as mean.
# impute column missing as mean, as each column is a snp.
for i in 1:size(X,2) #col
    m = mean([t for t in X[:,i] if !isnan(t)])
    for k in 1:size(X,1) #row
        if isnan(X[k,i])
            X[k,i] = m
        end
        ## shift allele to mean zero.
        X[k,i] -= m
    end
end

# println(X)
# convert to Z score by row.
# X = zscore(X,2)
#println(X)
#writedlm(Y)
#UNI_BETA="beta-00.txt"
UNI_BETA="sum.beta.txt" #beta from summary.
beta = readdlm(UNI_BETA,'\t',Float64,'\n')
# No beta addjusted prs.
if ONLY_PRS
    prs = X * beta
    writedlm(OUT_PREFIX * ".prs.txt",prs)
    exit(0)
end

# compute the the reweighted beta.
# new_beta = (X'X)^-1(X'Y) = (X'X)^-1 * diag(xi'xi) * old_beta
# if inv is not stable for real snp data, may try pinv.

# variance co-variance matrix of X.
cov_m = X'X

# generate diag(xi'xi)
d_matrix = zeros(size(cov_m,1),size(cov_m,1))
for i in 1:size(cov_m,1)
    d_matrix[i,i] = cov_m[i,i]
end

# new adjusted beta
new_beta = pinv(cov_m) * d_matrix * beta
if OUT_BETA
    writedlm(OUT_PREFIX * ".multi_beta.txt",new_beta)
end

# new PRS: X * new_beta
if OUT_PRS
    prs = X * new_beta
    writedlm(OUT_PREFIX * ".prs.txt",prs)
end

# PCA regression
prs = X * new_beta
# https://docs.julialang.org/en/v1/stdlib/LinearAlgebra/index.html
F = eigen(cov_m)
# sort the eigen values from big to small.
eigen_v = F.values[end:-1:1]
eigen_vt = F.vectors[:,end:-1:1]

# select top n eigen vectors.
top_n = 100
vk = eigen_vt[:,1:top_n]
wk = X*vk
# regress on the top pcs.
rk = inv(wk'*wk)*wk'*prs
# real y.
# It's near the sample performance by using real y, or restored y from beta.
#y = readdlm("y-00.txt",'\t',Float64,'\n')
#y = y .- mean(y)
#rk = inv(wk'*wk)*wk'*y

# pcr reverse beta.
p_beta = vk*rk
p_beta_out="00"
writedlm(p_beta_out * ".pbeta.txt",p_beta)
