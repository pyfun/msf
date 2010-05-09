import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import matplotlib.mlab as mlab

class ChisqTest:
    """
    Perform various chi-square tests.
    TODO: implement two variable independence test

    """
    def __init__(self,a):
        """
        a - the number of observations in each category
        """
        self.a = a
        self.nobs = np.sum(a)
        self.ncat = len(a)
        self.testone()
            
    def testone(self,p=None,dof=None,size=0.05):
        """
        Chi-Square test for one variable.

        p - the probability of each category
        """
        # only one puppet category
        if (not dof):
            self.dof = len(self.a) - 1
        else:
            self.dof = dof
        # if p is not given, uniform distribution
        if (p is None):
            self.p = 1./self.ncat
        else:
            self.p = p

        self.e = np.ones(self.ncat)*float(self.nobs)*self.p
        self.size = size
        # calculate chi-square score
        self.chisq = np.sum((self.e-self.a)**2/self.e)
        cdf = stats.chi2.cdf(self.chisq,self.dof)
        self.chisqc = stats.chi2.isf(self.size,self.dof)
        self.pvalue = 1-cdf
        # print test
        if (cdf>=1-size):
            self.result = 0
            print 'Rejected'
        else:
            self.result = 1
            print 'Accepted'






    def waldtest(self,a,omega,size=0.05):
        """
        Test if the ols coefficients a_1=a_2=0.
        a - coef
        omega - var-cov matrix
        size - test size
        """
        p = len(a)
        w = np.dot(a.T,np.linalg.solve(omega,a))
        cdf = stats.chi2.cdf(w,p)
        if (cdf>=1-size):
            print 'Rejected'
        else:
            print 'Accepted'
        return w,cdf

if __name__ == '__main__':
    import numpy as np
    a = np.array([5065,7779])
    chitest = ChisqTest(a)
    print chitest.chisq, chitest.e, chitest.pvalue
    # example in 068 birthday
    b = np.array([4,12,4,8,10,7])
    chitest = ChisqTest(b)
    print chitest.chisq, chitest.e, chitest.pvalue        
    chitest.testone(size=0.01)
    print chitest.chisq, chitest.e, chitest.pvalue    
