
cat test.txt | Rscript MultipleLinearRegression.R

[1] "FORMULA:"             "prestige~census+type"


Call:
lm(formula = as.formula(form), data = dd)

Residuals:
      1       2       3       4       5
 2.6673  6.3056 -3.1337 -6.3056  0.4664

Coefficients:
             Estimate Std. Error t value Pr(>|t|)
(Intercept) 54.980816  11.238070   4.892   0.0393 *
census       0.006915   0.008769   0.789   0.5130
typeprof     3.455825   6.912959   0.500   0.6667
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 6.952 on 2 degrees of freedom
Multiple R-squared:  0.4126,    Adjusted R-squared:  -0.1747
F-statistic: 0.7025 on 2 and 2 DF,  p-value: 0.5874
