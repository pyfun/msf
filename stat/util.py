import matplotlib.pyplot as plt
import numpy as np
        
def summaryone(x):
    """Summary of the time series.
    include mean, std, max, min and range
    """
    print 'mean and std are ',np.mean(x), np.std(x)
    print 'max and min are ',np.max(x), np.min(x)
    print 'the range is ',np.max(x)-np.min(x)
    
def plotone(x,y,xlabel,ylabel,filename):
    """Plot and save one time series.

    Usage:

    >>>plotone(x,y,'months','income','p1a.eps')
    """
    fig=plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x,y,linewidth=2.0)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    fig.savefig(filename)

def plothist(x,xlabel,ylabel,filename):
    """Plot histgrams.

    Usage:

    >>>plothist(x,'months','income','p1a.eps')
    """
    fig=plt.figure()
    ax = fig.add_subplot(111)
    
    n, bins, patches = ax.hist(x, 50, normed=True,facecolor='green', alpha=0.75)
    # hist uses np.histogram under the hood to create 'n' and 'bins'.
    # np.histogram returns the bin edges, so there will be 50 probability
    # density values in n, 51 bin edges in bins and 50 patches.  To get
    # everything lined up, we'll compute the bin centers
    bincenters = 0.5*(bins[1:]+bins[:-1])
    # add a 'best fit' line for the normal PDF
    mu = np.mean(x)
    sigma = np.std(x)
    y = mlab.normpdf( bincenters, mu, sigma)
    l = ax.plot(bincenters, y, 'r--', linewidth=2)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    #ax.set_title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
    ax.set_xlim(np.min(x), np.max(x))
#    ax.set_ylim(0, 0.03)
    ax.grid(True)
    fig.savefig(filename)

def plottwo(x,y1,y2,y1label,y2label,xlabel,ylabel,filename):
    """
    Plot two series in one plot.

    Usage:

    <<< plottwo(x,y1,y2,'Squared','Absolute value','lags','SSE','p1b.eps')
    """
    fig=plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x,y1,'ro-',linewidth=2.0,label=y1label)
    ax.plot(x,y2,'gs--',linewidth=2.0, label=y2label)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.legend()
    fig.savefig(filename)
