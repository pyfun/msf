import csv
import numpy as np

class TDX(object):
    def __init__(self, filename):
        """
        the volume in tdx is in shou (100gu)
        the amount in tdx is RMB yuan
        filename in format table19990131.txt
        """
        areader = csv.reader(open(filename),delimiter='\t')
        areader.next()
        data = [[row[0],row[11],row[13],row[14],row[3],
         row[7],row[16]] for row in areader
        if (not row[2].startswith('--'))]
        self.daypricesnap = np.array(data)
        self.date = filename[-8:] #'19990131'

    def savesnap(self,hdfname):
        with h5py.File(hdfname,'a') as daysnap:
            try:
                year = daysnap[self.date[:4]]
            except KeyError:
                year = daysnap.create_group(self.date[:4])
            try:
                month = year[self.date[4:6]]
            except KeyError:
                month = year.create_group(self.date[4:6])
            month[self.date[-2:]] = self.daypricesnap

    def savedayprice(self,hdfname):
        with h5py.File(hdfname,'a') as dayprice:
            for pricedata in self.daypricesnap:
                if (pricedata[0].startswith('60') or
                     pricedata[0].startswith('30')):
                    shprice = dayprice['SHA']
                    self._processhdf(shprice,pricedata)
                else:
                    shprice = dayprice['SHE']
                    self._processhdf(shprice,pricedata)
                    
        

    def _processhdf(self,shprice,pricedatarow):
        name = pricedatarow[0]
        print name
        try:
            shstockprice = shprice[name]
        except KeyError:
            shstockprice = shprice.create_group(name)
            print 'created',name
        try:
            histnode = shstockprice[self.date[:4]]
            histprice = np.array(histnode)
            del shprice[self.date[:4]]
            histprice = np.row_stack((histprice,pricedata))
            shprice[self.date[:4]] = histprice
        except KeyError:
            shprice[self.date[:4]] = pricedatarow

                                                
