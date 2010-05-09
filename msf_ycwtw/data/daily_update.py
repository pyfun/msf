import h5py
from lxml.html import parse
import numpy as np

class YahooData(object):
    """
    get chinese stock price from yahoo china.
    """
    dayurl = "http://yahoo.compass.cn/stock/xml/%s_day.xml" # 000671.sz
    weekurl = "http://yahoo.compass.cn/stock/xml/%s_week.xml" # 000671.sz
    monthurl = "http://yahoo.compass.cn/stock/xml/%s_month.xml" # 000671.sz

    @staticmethod
    def _gettree(url,stocksymbol):        
        tree = etree.parse(url % (stocksymbol.lower(),))
        for item in tree.xpath("//item"):
            yield item
    @staticmethod
    def getpricearray(stocksym):
        """
        update db from the yahoo xml item
        """
        repeat = True
        falsetime=0
        while(repeat):
            try:
                tree=_gettree(YahooData.dayurl,stocksym)
                for item in tree:
                    pricearray=np.array([[i[0].text,i[1].text,i[2].text,i[3].text,i[4].text,
                      i[5].text,i[6].text] for i in item.getchildren()])
                repeat = False                
            except:
                print 'try',stocksym,'one more time'
                falsetime += 1
            if (falsetime>20):
                print 'too many errors',stocksym
                repeat = False
        return pricearray
    
class SinaData(object):
    sina_history = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%s.phtml' #000671,sh600000
    sina_trades_csv = 'http://market.finance.sina.com.cn/downxls.php?date=%s&symbol=%s' #2010-04-21, sz000671
    with h5py.File('hdf/stockname_cn.hdf5','r') as stockname:
        # /SHA/A,/B, /SHE/A /CHINEXT /SME /B
        shaname = np.array(stockname['SHA']['A'])
        shbname = np.array(stockname['SHA']['B'])
        szaname = np.array(stockname['SHE']['A'])
        szsmename = np.array(stockname['SHE']['SME'])
        szchinextname = np.array(stockname['SHE']['CHINEXT'])
        
    @classmethod
    def processhdf(shprice,name):
        print name
        currentprice = getdayprice(name)
        if (len(currentprice)<1): return
        try:
            shstockprice = shprice[name]
        except KeyError:
            shstockprice = shprice.create_group(name)
        try:
            histnode = shstockprice[currentprice[0][0][:4]]                
            histprice = np.array(histnode)
            del shstockprice[currentprice[0][0][:4]]
            lastdate = histprice[-1][0]
            for dayp in np.flipud(currentprice):
                if (dayp[0]>lastdate): histprice = np.row_stack((histprice,dayp))
            shstockprice[currentprice[0][0][:4]] = histprice
        except KeyError:
            shstockprice[currentprice[0][0][:4]] = currentprice
            
        
    @classmethod
    def updatedayprice_sh():
        """
        update daily database in shanghai A and B shares
        """
        with h5py.File('hdf/dayprice_cn.hdf5','a') as dayprice:
            shprice = dayprice['SHA']
            # doing sh A shares
            [processhdf(shprice,name) for name in shaname[:,0]]
            print 'done update with Sh A shares'
            [processhdf(shprice,name) for name in shbname[:,0]]            
            print 'done update with Sh B shares'

    @classmethod            
    def updatedayprice_sz():
        with h5py.File('hdf/dayprice_cn.hdf5','a') as dayprice:        
            # doing sz shares
            shprice = dayprice['SHE']
            # doing sz A shares
            [processhdf(shprice,name) for name in szaname[150:,0]]                        
            print 'done update with Sz A shares'

    @classmethod            
    def updatedayprice_sme():
        with h5py.File('hdf/dayprice_cn.hdf5','a') as dayprice:
            shprice = dayprice['SHE']            
            for name in szsmename[:,0]:
                print name
                currentprice = getdayprice(name)
                if (len(currentprice)<1): continue                
                shstockprice = shprice[name]
                histnode = shstockprice[currentprice[0][0][:4]]                
                histprice = np.array(histnode)
                del shstockprice[currentprice[0][0][:4]]
                lastdate = histprice[-1][0]
                for dayp in np.flipud(currentprice):
                    if (dayp[0]>lastdate): histprice = np.row_stack((histprice,dayp))
                shstockprice[currentprice[0][0][:4]] = histprice
            print 'done update with Sz SME shares'

    @classmethod            
    def updatedayprice_chinext():
        with h5py.File('hdf/dayprice_cn.hdf5','a') as dayprice:
            shprice = dayprice['SHE']                        
            for name in szchinextname[:,0]:
                print name
                currentprice = getdayprice(name)
                if (len(currentprice)<1): continue                
                shstockprice = shprice[name]
                histnode = shstockprice[currentprice[0][0][:4]]                
                histprice = np.array(histnode)
                del shstockprice[currentprice[0][0][:4]]
                lastdate = histprice[-1][0]
                for dayp in np.flipud(currentprice):
                    if (dayp[0]>lastdate): histprice = np.row_stack((histprice,dayp))
                shstockprice[currentprice[0][0][:4]] = histprice
            print 'done update with Sz ChiNext shares'
                
                

    @classmethod
    def getdayprice(name):
        """
        return a price array for the name, include 7 daily price ohlcva
        """
        url = sina_history % (name,)
        repeat = True
        falsecount = 0
        while (repeat):
            try:
                tree = parse(url)
                subtree = tree.xpath('//table[@id="FundHoldSharesTable"]//div')
                pricearray=np.array([[subtree[i*7].getchildren()[0].text.strip().replace('-',''),
                    subtree[i*7+1].text,subtree[i*7+2].text,subtree[i*7+4].text,
                    subtree[i*7+3].text,float(subtree[i*7+5].text)/10000,
                    float(subtree[i*7+6].text)/10000] for i in range(1,min(6,len(subtree)/7-1))])
                repeat = False
            except:
                falsecount += 1
                if (falsecount>20): print 'get price wrong with %s' % (name,)
        return pricearray

                                   
if __name__ == '__main__':
    SinaData.updatedayprice_sh()
    SinaData.updatedayprice_sme()
    SinaData.updatedayprice_sz()
    SinaData.updatedayprice_chinext()    
