from bootstrap import BootStrap
import numpy as np

a=np.array([1.2,3.5,4.7,7.3,8.6,12.4,13.8,18.1])
print 'the length is',len(a)

def trim_mean(x):
    a=np.sort(x)
    n=len(x)
    return np.mean(a[n/4:n*3/4])

seeall = np.zeros((10,6))
for j in range(10):
    np.random.seed()

    B=[25,100,200,500,1000,2000]
    se = np.zeros(len(B))
    for i in range(len(B)):
        bs = BootStrap(a,B[i])
        bs.setestimator(trim_mean)
        bs.estimate()
        se[i] = bs.se

    seeall[j,:] = se

print seeall
    
