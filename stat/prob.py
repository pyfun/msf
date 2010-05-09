import scipy.stats as stat

# bionomial, draw with replacement
binompdf = stat.binom.pmf
binomcdf = stat.binom.cdf
# hypergeometric, draw without replacement
hypergeompdf = stat.hypergeom.pmf
hypergeomcdf = stat.hypergeom.cdf
