# PRS based on true beta.
# Let X is matrix, nxm, n is the number of samples, m is the number of snps, n>m.
# In a chr block, we have a multi-linear regression Xb = Y.
# LSQ solution for this: b = (X'X)^-1X'Y.
# Define PRS = P = Xb = X(X'X)^-1X'Y = X(X'X)^-1(n'beta)
# beta = [b1, b2, ... bn] is the univariant regression coefficient.
# bi = (Xi'Xi)^-1XiY = XiY/n*var(X). var(X) = 1, if X normalized, n is the sample size.

# test this PRS defination by taking Y, X and beta(marginal).

using DelimitedFiles
using LinearAlgebra

#println("hello world")
X = readdlm("x_matrix.txt",'\t',Float64,'\n')
beta = readdlm("beta_matrix.txt",'\t',Float64,'\n')

# compute the the estimated PRS.
# n*X(X'X)^-1beta
# the number of samples.
# if inv is not stable for real snp data, may try pinv.
n = size(X)[1]
prs = n * X * inv(X'X) * beta

writedlm("prs.txt",prs)
