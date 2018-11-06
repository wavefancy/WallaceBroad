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
for i in 1:size(X,1)
    m = mean([t for t in X[i,:] if !isnan(t)])
    for k in 1:size(X[i,:],1)
        if isnan(X[i,k])
            X[i,k] = m
        end
    end
end

# println(X)
# convert to Z score by row.
X = zscore(X,2)
#println(X)
#writedlm(Y)
beta = readdlm("beta.txt",'\t',Float64,'\n')

# compute the the estimated PRS.
# n*X(X'X)^-1beta
# the number of samples.
# if inv is not stable for real snp data, may try pinv.
n = size(X)[1]
t = X'*X
println(size(t))
println(det(t))
#prs = n * X * pinv(t) * beta
#start with rigous version.
prs = n * X * inv(t) * beta

writedlm("prs.txt",prs)
