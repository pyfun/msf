"""Tools for discretized Brownian motion"""

from __future__ import division
import numpy as np

class MultiPath(object):
    
    def __init__(self, Wt, dt):
        self.Wt = Wt
        self.dt = dt
        
    def ofSize(numPaths, numIncrs, dt):
        """Create MultiPath with random increments"""
        mi = MultiIncrements.ofSize(numPaths, numIncrs, dt)
        return mi.toPaths()
    ofSize = staticmethod(ofSize)

    def expandInterval(self, R):
        """Return a new MultiPath instance with dt expanded to R*dt"""
        return MultiPath(self.Wt[:,::R], R * self.dt)
        
    def toIncrements(self):
        """Convert paths to a MultiIncrements instance"""
        pv = self.Wt
        incrs = N.subtract(pv[:,1:], pv[:,:-1])
        return MultiIncrements(incrs, self.dt)
    
    def toPaths(self):
        """Return Brownian motion as paths.
        
        This is a null operation, just returning the instance itself. 
        It is included to allow commonality of interface between
        MultiPath and MultiIncrements."""
        return self
            
class MultiIncrements(object):
    """Discretized Brownian motion represented by increments"""
    def __init__(self, dWt, dt):
        self.dWt = dWt
        self.dt = dt
        
    def ofSize(numPaths, numIncrs, dt):
        """Create MultiIncrements with random increments"""
        return MultiIncrements(RA.normal(0, N.sqrt(dt), (numPaths, numIncrs)),
                               dt)
    ofSize = staticmethod(ofSize)
        
    def expandInterval(self, R):
        """Return new MultiIncrements instance with dt expanded to R*dt"""
        return self.toPaths().expandInterval(R).toIncrements()
                
    def toIncrements(self):
        """Return Brownian motion as increments.
        
        This is a null operation, just returning the instance itself. 
        It is included to allow commonality of interface between
        MultiPath and MultiIncrements."""
        return self
    
    def toPaths(self):
        """Convert increments to a MultiPath instance"""
        incrs = self.dWt
        vals = N.concatenate((N.zeros((incrs.shape[0], 1)), 
                              N.cumsum(incrs, axis=1)),
                              axis=1)
        return MultiPath(vals, self.dt)
        
def sdeEM(f, g, X0, dbm):
    """Approximate solution to SDE using the Euler-Maruyama method.
    
    This is specialized for a scalar, autonomous SDE. The SDE is 
    integrated with the discrete Brownian paths described by the
    dbm object, which is assumed to be an instance of either 
    MultiIncrements or MultiPath."""
    
    mulIncr = dbm.toIncrements()
    dt = mulIncr.dt
    dWt = mulIncr.dWt
    paths, steps = N.shape(dWt)
        
    t = N.concatenate(([0.0], N.cumsum(N.resize([dt], steps))))
    Xt = N.zeros((paths, steps+1), N.Float)
    Xt[:,0] = prevX = X0

    for n in xrange(0, steps):
        nextX = prevX + f(prevX) * dt + g(prevX) * dWt[:,n]
        Xt[:,n+1] = nextX
        prevX = nextX
        
    return t, Xt
    
def sdeMilstein(f, g, dg, X0, dbm):
    """Approximate solution to SDE using Milstein's method.
    
    This is specialized for a scalar, autonomous SDE. The SDE is 
    integrated with the discrete Brownian paths described by the
    dbm object, which is assumed to be an instance of either 
    MultiIncrements or MultiPath."""
    
    mulIncr = dbm.toIncrements()
    dt = mulIncr.dt
    dWt = mulIncr.dWt
    paths, steps = N.shape(dWt)
        
    t = N.concatenate(([0.0], N.cumsum(N.resize([dt], steps))))
    Xt = N.zeros((paths, steps+1), N.Float)
    Xt[:,0] = prevX = X0

    for n in xrange(0, steps):
        dW = dWt[:,n]
        gX = g(prevX)
        nextX = prevX + f(prevX) * dt + gX * dW \
                    + 0.5 * gX * dg(prevX) * (dW ** 2 - dt)
        Xt[:,n+1] = nextX
        prevX = nextX
        
    return t, Xt
    
