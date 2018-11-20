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
# Let X is matrix, nxm, n is the number of samples, m is the number of snps, n>m.
X = readdlm("x.txt",',',Float64,'\n')
# replace NaN missing as mean.
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
#X = zscore(X,2)
#println(X)
#writedlm(Y)
y = readdlm("y.txt",'\t',Float64,'\n')
# my = mean(y)
# substract y's mean.
y = y .- mean(y)
# Single variant regress,
# *** x and y has to be mean centered.
# b = (x'x)^-1X'Y
B = zeros(size(X,2),1)
for i in 1:size(X,2)
    # k = X[:,i] .- mean(X[:,i])
    k = X[:,i] # X is already shift to mean zero above, ignore this.
    b = inv(k'*k)*k'* y
    B[i] = b[1]
end

writedlm("res_b.txt",B)
