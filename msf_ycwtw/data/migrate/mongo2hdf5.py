import numpy as np
import h5py
from mongo import *
import time

# f1 = h5py.File('stockname.hdf5','w')
# start = time.time()
# for item in Stock.objects:
#     if (not item.province): item.province=' '
#     a=np.char.array([item.name.encode('utf8'),item.goosym,item.bsymid,
#                      item.province.encode('utf8'),item.sector,item.industry])
#     f1[item.sym]=a
# f1.close()
# print 'cost',time.time()-start
f1 = h5py.File('dayprice_cn.hdf5','a')
#sh = f1.create_group('SHA')
#sz = f1.create_group('SHE')
sh=f1['SHA']
for item in Stock.objects(sym__startswith='601'):
    stock=sh.create_group(item.sym[:6])
    pricearray=[]
    for price in PriceDay.objects(sym__startswith=item.sym):
        pricearray.append([price.sym[10:],price.o,price.h,price.l,price.c,price.v,price.a])
    pricearray=np.flipud(np.char.array(pricearray))
    for date in set([i[:4] for i in pricearray[:,0]]):
        a = pricearray[pricearray[:,0].startswith(date)]
        stock[date] = a
# for item in Stock.objects(sym__startswith='30'):
#     stock=sz.create_group(item.sym[:6])
#     pricearray=[]
#     for price in PriceDay.objects(sym__startswith=item.sym):
#         pricearray.append([price.sym[10:],price.o,price.h,price.l,price.c,price.v,price.a])
#     pricearray=np.flipud(np.char.array(pricearray))
#     for date in set([i[:4] for i in pricearray[:,0]]):
#         a = pricearray[pricearray[:,0].startswith(date)]
#         stock[date] = a

# for item in Stock.objects(sym__startswith='00'):
#     stock=sz.create_group(item.sym[:6])
#     pricearray=[]
#     try:
#         for price in PriceDay.objects(sym__startswith=item.sym):
#             pricearray.append([price.sym[10:],price.o,price.h,price.l,price.c,price.v,price.a])
#         pricearray=np.flipud(np.char.array(pricearray))
#         #    
#         for date in set([i[:4] for i in pricearray[:,0]]):
#             a = pricearray[pricearray[:,0].startswith(date)]
#             stock[date] = a
#     except:
#         pricearray=[]
#         for price in PriceDay.objects(sym__startswith=item.sym.lower()):
#             pricearray.append([price.sym[10:],price.o,price.h,price.l,price.c,price.v,price.a])
#         pricearray=np.flipud(np.char.array(pricearray))
#         #    
#         for date in set([i[:4] for i in pricearray[:,0]]):
#             a = pricearray[pricearray[:,0].startswith(date)]
#             stock[date] = a

        
f1.close()

