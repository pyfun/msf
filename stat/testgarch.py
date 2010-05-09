import csv
import numpy as np
from garch import Garch

aReader = csv.reader(open('GSCI_Return.csv','rb'),delimiter=',')
data = [[date,float(o.replace(",","")),float(h.replace(",","")),
         float(l.replace(",","")),float(c.replace(",",""))] for date,o,h,l,c in aReader]
darray = np.array(data)
gsci = darray[:,-1].astype(float)
gscidate = darray[:,0]

gsci_ret = np.log(gsci[1:]/gsci[:-1])
tg = Garch(gsci_ret,[0.01,0.04,0.])
print tg.coef
