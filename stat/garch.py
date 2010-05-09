import numpy as np
from scipy.optimize import fmin_cobyla
from scipy import stats



class Garch(object):
    """
    garch volatility models. Try to use OpenOpt to optimize the
    likelihood function.
    """
    def __init__(self,dat,x0):
        """
        dat is the time series Tx1.
        x0 is the initial guess [alpha,beta,constant]
        """
        self.ts = dat
        self.T = len(self.ts)
        self.sigma_sqr = np.zeros(self.T)
        self.coef = self.garchfit(x0)
        tmp = self.f(self.coef)
        self.res = self.ts/np.sqrt(self.sigma_sqr)

    def archtest(self):
        """
        Perform engle's test.
        """
        pass


    def f(self,x):
        """
        Compute logged likelihood function given a time series of residuals 
        and parameters for GARCH(1,1) process:
        sigma(t)^2 = omega + beta * sigma(t-1)^2 + alpha * ita(t)^2
        ita(t+1) = sigma(t) * e(t+1)
        where e(t) are i.i.d standard normal RVs
        ------------------------------------------------------------------------
        RETURNS:
        L = -(logged Likelihood)
        """
        alpha = x[0]
        beta = x[1]
        omega = x[2]

        self.sigma_sqr = np.zeros(self.T)

        # set sigma_0 square to be unconditional variance
        self.sigma_sqr[0] = np.cov(self.ts)

        # Calculate conditional variance
        for t in xrange(1,self.T):
            self.sigma_sqr[t] = omega + beta*self.sigma_sqr[t-1] + alpha*self.ts[t-1]**2


        L = -0.5*(np.log(2*np.pi)+(self.ts**2)/self.sigma_sqr+np.log(self.sigma_sqr))
        return -np.sum(L)

    def garchfit(self,initvalue):
        """
        estimate GARCH(1,1) paramters by maximum likelihood method. 
        Optimization should be under the following constraints:
        ARCH + GARCH < 1 (Stationarity)
        All parameters >= 0 (Non-negative)
        -------------------------------------------------------------------------
        InitValue = [ARCH; GARCH; Constant]
        """

        try:
            from openopt import NLP
            lb = [0.0001, 0.0001, 0.] #lower bound
            A = [1, 1, 0]
            b = 1.0
            p = NLP(self.f,initvalue,lb=lb,A=A,b=b)
            r = p.solve('ralg')
        
            return r.xf
        except ImportError:
            print "Openopt is not installed, will use scipy.fmin_cobyla instead"
            print "the result may not accurate though"
            params = fmin_cobyla(self.f,initvalue,cons=[lambda x:1-(x[0]+x[1]),
                                                   lambda x:x[0],
                                                   lambda x:x[2],
                                                   lambda x:x[1]])
            return params

    def garchse(self,x):
        """
        Compute standard errors from GMM and MLE

        Usage:

        Return v_gmm and v_mle, covariance matrix
        """
        alpha = x[0]
        beta = x[1]
        omega = x[2]

T = length(ita); % Length of the time series of residuals
SigmaSqr = zeros(T,1); % T x 1 vector of sigma(t), t = 0,...,T-1
h = zeros(3,T); % 3 x T matrix, h(:,t) is h(t)
h_deri = zeros(3,3,T); % 3 x 3 x T matrix, h(:,:,t) is derivative of h

SigmaSqr(1) = var(ita); %Set (sigma_0)^2 to be unconditional variance

for t = 2:T
    SigmaSqr(t) = omega + beta*SigmaSqr(t-1) + alpha*ita(t-1)^2;
end

%See attached document for the formulae of computing the deriviative
%iteratively

Deri1 = zeros(3,1); %dSigmaSqr/dPara
Deri2 = zeros(3,3); %d^2SigmaSqr/dPara^2

for t = 1:T
    h(:,t) = 0.5/SigmaSqr(t)*(ita(t)^2/SigmaSqr(t)-1)*Deri1;
    h_deri(:,:,t) = 0.5/SigmaSqr(t)*(ita(t)^2/SigmaSqr(t)-1)*Deri2+...
                    (0.5-ita(t)^2/SigmaSqr(t))/SigmaSqr(t)^2*Deri1*Deri1';
    Deri2 = beta*Deri2 + [0 Deri1(1) 0;Deri1(1) 2*Deri1(2) Deri1(3);0 Deri1(3) 0];
    Deri1 = beta*Deri1 + [ita(t)^2;SigmaSqr(t);1];
end

D = zeros(3,3); %Sample mean of h_deri
S = zeros(3,3); %Sample covariance of h
for t = 1:T
    D = D + h_deri(:,:,t);
    S = S + h(:,t)*h(:,t)';
end

D = D'/T;
S = S/T;

V_GMM = inv(D*inv(S)*D')/T; %Asymptotic covariance of estimates in GMM framework
V_MLE = inv(S)/T; %Asymptotic covariance of estimates in MLE framework
        pass

            

