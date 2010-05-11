import csv
import h5py
import numpy as np

class TDX(object):
    """
    save data from TDX to hdf

    todo: save data to redis

    use:
    >>> a=TDX('tablea20100507')
    >>> a.savesnap2hdf('hdf/snapdayprice_cn.hdf5')
    >>> a.savedayprice2hdf('hdf/dayprice_cn.hdf5')
    """
    def __init__(self, filename):
        """
        the volume in tdx is in shou (100gu)
        the amount in tdx is RMB yuan
        filename in format table19990131, no extension
        """
        areader = csv.reader(open(filename),delimiter='\t')
        areader.next()
        data = [[row[0],row[11],row[13],row[14],row[3],
         float(row[7])/100,float(row[16])/10000] for row in areader
        if (not row[16].startswith('--'))]
        self.daypricesnap = np.array(data)
        self.date = filename[-8:] #'19990131'

    def savesnap2hdf(self,hdfname):
        with h5py.File(hdfname,'a') as daysnap:
            try:
                year = daysnap[self.date[:4]]
            except KeyError:
                year = daysnap.create_group(self.date[:4])
            try:
                month = year[self.date[4:6]]
            except KeyError:
                month = year.create_group(self.date[4:6])
            try:
                histnode = month[self.date[-2:]]
                histprice = np.array(histnode)
                del month[self.date[-2:]]
                histprice = np.row_stack((histprice,self.daypricesnap))
            except:
                histprice = self.daypricesnap
            month[self.date[-2:]] = histprice

    def savedayprice2hdf(self,hdfname):
        with h5py.File(hdfname,'a') as dayprice:
            for pricedata in self.daypricesnap:
                if (pricedata[0].startswith('60') or
                     pricedata[0].startswith('90')):
                    shprice = dayprice['SHA']
                    self._processhdf(shprice,pricedata)
                else:
                    shprice = dayprice['SHE']
                    self._processhdf(shprice,pricedata)
                    
        

    def _processhdf(self,shprice,pricedatarow):
        name = pricedatarow[0]
        pricedatarow[0]=self.date
        try:
            shstockprice = shprice[name]
        except KeyError:
            shstockprice = shprice.create_group(name)
            print 'created',name
        try:
            histnode = shstockprice[self.date[:4]]
            histprice = np.array(histnode)
            if (histprice[-1][0]<self.date):            
                del shstockprice[self.date[:4]]
                histprice = np.row_stack((histprice,pricedatarow))
                shstockprice[self.date[:4]] = histprice
                print 'updated',name
        except KeyError:
            shstockprice[self.date[:4]] = pricedatarow

                                                
