import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from ols import ols

def brownian_path(T,N):
    """
    return brownian motion path
    """
    dt = float(T)/N

    dW = np.sqrt(dt)*np.random.randn(N)
    dW[0] = 0
    W = np.cumsum(dW)
    return W
def brownian_path2(T,N):
    """
    return brownian motion path
    """
    dt = float(T)/N
    for i in range(5000):
        dW = np.sqrt(dt)*np.random.randn(N)
        dW[0] = 0
        dW2 = -dW
        W = np.cumsum(dW)
        W2 = np.cumsum(dW2)
        yield W
        yield W2

def asian_path(K):
    T=1.; J=252; dt=T/J
    mu=0.1; sigma=0.3; r=0.05
    s0=100.
    sim = 10000
    level = 0.05

    path = [s0 * np.exp(np.linspace(dt,T,J)*(r-sigma**2/2) +
                   sigma*brownian_path(T,J)) for i in range(sim)]
    price = np.zeros(sim)
    ii = 0
    for s in path:
        price[ii]=np.exp(-r*T)*np.maximum(0,np.mean(s)-K)
        ii += 1
    plt.figure(2)
    plt.hist(price)
    results = np.sort(price)
    ci = (results[int(sim * (1 - level))],
                results[int(sim * level)])
    return np.mean(price),np.std(price),ci
def asian_path_antithetic(K):
    T=1.; J=252; dt=T/J
    mu=0.1; sigma=0.3; r=0.05
    s0=100.
    sim = 10000
    level = 0.05

    path = [s0 * np.exp(np.linspace(dt,T,J)*(r-sigma**2/2) +
                   sigma*a) for a in brownian_path2(T,J)]
    price = np.zeros(sim)
    ii = 0
    for s in path:
        price[ii]=np.exp(-r*T)*np.maximum(0,np.mean(s)-K)
        ii += 1
    plt.figure(2)
    plt.hist(price)
    results = np.sort(price)
    ci = (results[int(sim * (1 - level))],
                results[int(sim * level)])
    return np.mean(price),np.std(price),ci
def asian_path_control(K):
    T=1.; J=252; dt=T/J
    mu=0.1; sigma=0.3; r=0.05
    s0=100.
    sim = 500
    level = 0.05
    path = [s0 * np.exp(np.linspace(dt,T,J)*(r-sigma**2/2) +
                   sigma*brownian_path(T,J)) for i in range(sim)]
    pricey = np.zeros(sim)
    pricex = np.zeros(sim)

    ii = 0
    for s in path:
        pricey[ii]=np.exp(-r*T)*np.maximum(0,np.mean(s)-K)
        pricex[ii]=np.exp(-r*T)*np.maximum(0,s[-1]-K)
        ii += 1
    m = ols(pricey,pricex)
    print m.b
    print m.R2
    sim = 9500
    path = [s0 * np.exp(np.linspace(dt,T,J)*(r-sigma**2/2) +
                   sigma*brownian_path(T,J)) for i in range(sim)]
    pricey = np.zeros(sim)
    pricex = np.zeros(sim)
    price = np.zeros(sim)    
    ii = 0
    z1 = (np.log(s0/K)+(r+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    z2 = z1-sigma*np.sqrt(T)
    x_mean = s0*sp.stats.norm.cdf(z1) - np.exp(-r*T)*K*sp.stats.norm.cdf(z2)
    for s in path:
        pricey[ii]=np.exp(-r*T)*np.maximum(0,np.mean(s)-K)
        pricex[ii]=np.exp(-r*T)*np.maximum(0,s[-1]-K)
        price[ii] = pricey[ii]-m.b[-1]*(pricex[ii]-x_mean)
        ii += 1
    
    plt.figure(2)
    plt.hist(price)
    results = np.sort(price)
    ci = (results[int(sim * (1 - level))],
                results[int(sim * level)])
    return np.mean(price),np.std(price),ci
        

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

if __name__ == '__main__':
    for k in [80,100,120]:
        asian_path(k)
        asian_path_antithetic(k)
        asian_path_control(k)
