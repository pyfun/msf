from lxml.html import fromstring, tostring, open_in_browser
from lxml import etree
import csv
from mongo import *

class ChinaDayPrice(object):
    """
    get chinese stock price from yahoo china.
    """
    def __init__(self):
        self.dayurl = "http://yahoo.compass.cn/stock/xml/%s_day.xml" # 000671.sz
        self.weekurl = "http://yahoo.compass.cn/stock/xml/%s_week.xml" # 000671.sz
        self.monthurl = "http://yahoo.compass.cn/stock/xml/%s_month.xml" # 000671.sz

    def _gettree(self,url,stocksymbol):        
        tree = etree.parse(url % (stocksymbol.lower(),))
        for item in tree.xpath("//item"):
            yield stocksymbol,item

    def _update_mongo(self,stocksym):
        """
        update db from the yahoo xml item
        """
#        stocksym = (i.sym for i in Stock.objects.only('sym')[24:28])
        # try:
        #     for i in stocksym:
        #         for sym,item in self._gettree(self.dayurl,i):
        #             atag = item.getchildren()
        #             sym = sym +'.'+atag[0].text
        #             aprice = PriceDay(sym=sym, o=float(atag[1].text),h=float(atag[2].text),
        #                               l=float(atag[3].text),c=float(atag[4].text),
        #                               v=float(atag[5].text),a=float(atag[6].text))
        #             aprice.save()
        # except:
        #     print sym
        repeat = True
        falsetime=0
        while(repeat):
            try:
                tree=self._gettree(self.dayurl,stocksym)
                for sym,item in tree:
                    atag = item.getchildren()
                    sym = sym +'.'+atag[0].text
                    aprice = PriceDay(sym=sym, o=float(atag[1].text),h=float(atag[2].text),
                                      l=float(atag[3].text),c=float(atag[4].text),
                                      v=float(atag[5].text),a=float(atag[6].text))
                    aprice.save()
                repeat = False                
            except:
                print 'try',stocksym,'one more time'
                falsetime += 1
            if (falsetime>20):
                print 'too many errors',stocksym
                repeat = False
        
        
        
