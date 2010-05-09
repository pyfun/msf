import numpy as np

from numpy.random import standard_normal
from numpy import array, zeros, sqrt, shape
from matplotlib.pyplot import *

def brownian_path(T,N):
    dt = float(T)/N

    dW = sqrt(dt)*np.random.randn(N)
    dW[0] = 0
    W = np.cumsum(dW)
    return W

def brown():
    S0 = 10.222

    T =1
    dt =0.0002
    sigma = 0.4
    mu = 1
    N_Sim = 10

    Steps=round(T/dt); #Steps in years
    S = zeros([N_Sim, Steps], dtype=float)
    x = range(0, int(Steps), 1)

    for j in range(0, N_Sim, 1):
            S[j,0]= S0
            for i in x[:-1]:
                    S[j,i+1]=S[j,i]+S[j,i]*(mu-0.5*pow(sigma,2))*dt+sigma*S[j,i]*sqrt(dt)*standard_normal();
            plot(x, S[j])

    title('Simulations %d Steps %d Sigma %.6f Mu %.6f S0 %.6f' % (int(N_Sim), int(Steps), sigma, mu, S0))
    xlabel('steps')
    ylabel('stock price')
    show()

def multiple_path():
    T=1.; N=500; dt=T/N
    path = (np.exp(np.linspace(dt,T,N)+0.5*brownian_path(1,500)) for i in range(10))
    total = np.zeros(N)
    figure(1)
    hold(True)
    for i in path:
        plot(range(500),i)
        total += i
    m = total/10
    plot(range(500),m,lw='5.0')
    show()
