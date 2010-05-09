import DiscreteBrownianMotion
import numarray as N

"""
Create discretized Brownian paths. We'll need the path values for 
calculating the exact solution, so we'll represent the discrete 
Brownian motion using MultiPath. This allows comparison of the numerical 
approximation with the exact solution.

We'll look at 5 paths with 1000 increments on each of the paths. The time
range is arbitrary; we take it to be [0, 1].
"""

dbm = DiscreteBrownianMotion.MultiPath.ofSize(5, 1000, .001)

"""
Solve the SDE. We define the f and g functions first, then pass them to
the solver. We also use the known solution for the SDE for comparison 
purposes.
"""

def f(x):
    return 2 * x
def g(x):
    return x

# numeric solutions
t, Xt = DiscreteBrownianMotion.sdeEM(f, g, 1, dbm)  
# exact solutions
Yt = N.exp(1.5*t + dbm.Wt)       

"""
Now use a different time interval for integration than for the discretized
Brownian motion. Just expand the time interval for the Brownian motion, and
repeat the integration.
"""

expandFactor = 10
dbm2 = dbm.expandInterval(expandFactor)
t2, Xt2  = DiscreteBrownianMotion.sdeEM(f, g, 1, dbm2)  

"""
Take a look at the results. We'll first examine the RMS error of the numeric
solution compared to the exact solution, and print the values determined.
"""

def rms(x,y): return N.sqrt(N.sum((x - y) ** 2, axis=1) / x.shape[1])
rmserr = rms(Xt, Yt)
rmserr2 = rms(Xt2, Yt[:,::10])

print "Integration step: dt"
print "RMS Error:", "".join(["%9.4f" % r for r in rmserr])
print
print "Integration step: %s*dt" % expandFactor 
print "RMS Error:", "".join(["%9.4f" % r for r in rmserr2])
print
print
print

"""
Now we plot the numeric and exact solutions, to allow a visual comparison.
We wrap the whole thing in a try-block to let the script run even if there
is a problem connecting to gnuplot.
"""

try:
    import Gnuplot
except ImportError:
    print "Unable to create graphs with gnuplot"
else:
    """
    Create interface to the gnuplot program.
    """
    
    gp = Gnuplot.Gnuplot()
    
    """
    Iterate through all the paths and plot the exact and numeric solutions.
    """
    
    gp.xlabel("t")
    gp.ylabel("Xt")
    for x, y in zip(Xt, Yt):
        gp.plot(Gnuplot.Data(t, x, with="lines", title="EM method")) 
        gp.replot(Gnuplot.Data(t, y, with="lines", title="Exact")) 
        raw_input("press return to continue")
    
    for x2, y in zip(Xt2, Yt):
        gp.plot(Gnuplot.Data(t2, x2, with="linespoints", title="EM method")) 
        gp.replot(Gnuplot.Data(t, y, with="lines", title="Exact")) 
        raw_input("press return to continue")
    
    
