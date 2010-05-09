import numpy as np
import h5py
from mongo import *

f1 = h5py.File('stockname_cn.hdf5','a')
# sh=f1.create_group('SHA')
# sha = sh.create_dataset('A',(860,6),'S20',maxshape=(None,None))
# namearray=[]
# for item in Stock.objects(sym__startswith='60'):
#     if (not item.province): item.province=' '
#     if (not item.sector): item.sector=' '
#     if (not item.industry): item.industry=' '
#     if (not item.bsymid): item.bsymid=' '    
    
#     namearray.append([item.sym[:6],item.name.encode('utf8'),item.province,
#                       item.sector, item.industry, item.bsymid])
# namearray=np.char.array(namearray)
# sha[:] = namearray

#sz=f1.create_group('SHE')
sz=f1['SHE']
numb1 = Stock.objects(sym__startswith='002').count()
numb2 = Stock.objects(sym__startswith='30').count()
szb = sz.create_dataset('CHINEXT',(numb2,6),'S20',maxshape=(None,None))
namearray=[]
for item in Stock.objects(sym__startswith='30'):
    if (not item.province): item.province=' '
    if (not item.sector): item.sector=' '
    if (not item.industry): item.industry=' '
    if (not item.bsymid): item.bsymid=' '    
    
    namearray.append([item.sym[:6],item.name.encode('utf8'),item.province.encode('utf8'),
                      item.sector, item.industry, item.bsymid])
    
namearray=np.char.array(namearray)
szb[:] = namearray

f1.close()
                
