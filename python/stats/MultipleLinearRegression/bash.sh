
cat test.txt | python3 MultipleLinearRegression.py 

#/home/wallace/miniconda3/lib/python3.6/site-packages/statsmodels/compat/pandas.py:56: FutureWarning: The pandas.core.datetools module is deprecated and will be removed in a future version. Please use the pandas.tseries module instead.
#  from pandas.core import datetools
#                            OLS Regression Results                            
#==============================================================================
#Dep. Variable:                      y   R-squared:                       0.535
#Model:                            OLS   Adj. R-squared:                  0.461
#Method:                 Least Squares   F-statistic:                     7.281
#Date:                Wed, 16 Aug 2017   Prob (F-statistic):            0.00191
#Time:                        16:55:18   Log-Likelihood:                -26.025
#No. Observations:                  23   AIC:                             60.05
#Df Residuals:                      19   BIC:                             64.59
#Df Model:                           3                                         
#Covariance Type:            nonrobust                                         
#==============================================================================
#                 coef    std err          t      P>|t|      [0.025      0.975]
#------------------------------------------------------------------------------
#x1             0.2424      0.139      1.739      0.098      -0.049       0.534
#x2             0.2360      0.149      1.587      0.129      -0.075       0.547
#x3            -0.0618      0.145     -0.427      0.674      -0.365       0.241
#const          1.5704      0.633      2.481      0.023       0.245       2.895
#==============================================================================
#Omnibus:                        6.904   Durbin-Watson:                   1.905
#Prob(Omnibus):                  0.032   Jarque-Bera (JB):                4.708
#Skew:                          -0.849   Prob(JB):                       0.0950
#Kurtosis:                       4.426   Cond. No.                         38.6
#==============================================================================
#
#Warnings:
#[1] Standard Errors assume that the covariance matrix of the errors is correctly specified
