# PRS based on true beta.
# Let X is matrix, nxm, n is the number of samples, m is the number of snps, n>m.
# In a chr block, we have a multi-linear regression Xb = Y.
# LSQ solution for this: b = (X'X)^-1X'Y.
# Define PRS = P = Xb = X(X'X)^-1X'Y = X(X'X)^-1(n'beta)
# beta = [b1, b2, ... bn] is the univariant regression coefficient.
# bi = (Xi'Xi)^-1XiY = XiY/n*var(X). var(X) = 1, if X normalized, n is the sample size.

# test this PRS defination by taking Y, X and beta(marginal).

using DelimitedFiles
using StatsBase
using Statistics
using LinearAlgebra

#println("hello world")
X = readdlm("x.txt",',',Float64,'\n')
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
beta = readdlm("beta.txt",'\t',Float64,'\n')

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
writedlm("new_beta.txt",new_beta)

# new PRS: X * new_beta
prs = X * new_beta
writedlm("prs.txt",prs)
