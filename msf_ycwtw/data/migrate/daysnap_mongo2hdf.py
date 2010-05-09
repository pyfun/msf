import numpy as np
import h5py
from mongo import *

f1 = h5py.File('snapdayprice_cn.hdf5','w')
for year in xrange(2010,2009,-1):
    f1year=f1.create_group(str(year))
    for month in xrange(12):
        m='%02d' % (month+1,)
        f1month=f1year.create_group(m)
        for day in xrange(31):
            dayy='%02d' % (day+1,)
            date='%d%02d%02d' % (year,month+1,day+1)
            pricearray=[]
            print date
            try:
                for price in PriceDay.objects(sym__endswith=date):
                    pricearray.append([price.sym[:6],price.o,price.h,price.l,price.c,price.v,price.a])
                pricearray=np.char.array(pricearray)
                if(len(pricearray)>0): f1month[dayy]=pricearray
            except:
                continue

f1.close()
                
