import numpy as np

class BootStrap(object):
    """
    Implement different bootstraping techniques.
    """
    def __init__(self,data,size):
        """data is the input sample and size is the number of  bootstrap samples
        The length of the bootstrap sample is the same as the original.
        """
        self.oldsample = data
        self.n = len(data)
        self.size = size
        self.newsample = np.zeros((self.n,self.size))
        self.setestimator()

    def setestimator(self,est=np.mean):
        """
        est is the function to calculate the estimator
        """
        self.estimator = est
        

    def estimate(self,level=0.95):
        """
        Estimate the statistics from bootstrap.
        """
        self.theta = self.estimator(self.oldsample)
        # resampling
        for i in range(self.size):
            ind = np.random.random_integers(0,self.n-1,self.n)
            self.newsample[:,i] = self.oldsample[ind]
        self.thetabs = np.array([self.estimator(self.newsample[:,i]) for i in range(self.size)])
        self.se = np.std(self.thetabs,ddof=1)
        
        results = np.sort(self.thetabs)
       	self.ci = (results[int(self.size * (1 - level))],
                results[int(self.size * level)])
