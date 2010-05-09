import urllib
from lxml.html import fromstring, tostring, open_in_browser
import csv
from mongo import *

class ChinaSZ(object):
    """
    extract stock info from excel (csv) file
    remove the last line in csv before run

    use:
    >>> a = ChinaSZ()
    >>> a.stockname #dict of stock
    >>> a.save_mongo() #save name to mongodb
    """
    def __init__(self):
        aReader = csv.reader(open('shenzhen.csv'))
        aReader.next()
        self.stockname = []
        stock = {}
        for row in aReader:
            if(len(row[6])>2):
                stock['name']=row[6].decode('gbk')
                stock['sym']=row[0].decode('gbk')
                stock['province']=row[11].decode('gbk')
                self.stockname.append(stock.copy())

    def save_mongo(self):
        """ save stock name data to mongodb
        """
        [Stock(name=stock['name'],sym=stock['sym']+'.SZ',province=stock['province'],
              goosym='SHE:'+stock['sym']).save() for stock in self.stockname]
        
        

class ChinaSH(object):
    """
    Chinese Shanghai stock exchange.
    
    use:
    >>> a = ChinaSH()
    >>> a.get_nameA()
    >>> a.get_nameB()
    >>> a.stocknameA, a.stocknameB # name dict
    >>> a.save_mongo() #save stock names to mongodb
    """
    def __init__(self):
        self.url = "http://www.sse.com.cn"
        self.url_name = "http://www.sse.com.cn/sseportal/webapp/datapresent/SSEQueryStockInfoAct?reportName=BizCompStockInfoRpt&PRODUCTID=&PRODUCTJP=&PRODUCTNAME=&keyword=&tab_flg=&CURSOR=%d"
        self.urlb = "http://www.sse.com.cn/sseportal/webapp/datapresent/SSEQueryStockInfoAct?keyword=&reportName=BizCompStockInfoRpt&PRODUCTID=&PRODUCTJP=&PRODUCTNAME=&CURSOR=%d&tab_flg=2"
        self.stocknameA = [] #A shares
        self.stocknameB = [] #B shares

    def parse_name(self,url,stockdict):
        """append stock names to the list
        """
        stock = {}
        f = urllib.urlopen(url)
        data = f.read()
        f.close()
        # to unicode
        data = data.decode('GB2312')
 
        html = fromstring(data)
        table = html.xpath('//table[@cellpadding="2"]')[0]
        for ii in table.iter('tr'):
            aa=ii.getchildren() #<td>
            try:
                bb = aa[0].getchildren()
                stock['sym'] = bb[0].text
                stock['name']=aa[1].text
                stockdict.append(stock.copy())                
            except:
                pass
        
        
    def get_nameA(self):
        stock = {} # name and symbol
        # extract the number of pages
        f = urllib.urlopen(self.url_name % (1,))
        data = f.read()
        f.close()
        # to unicode
        data = data.decode('GB2312')
 
        html = fromstring(data)
        npage = int(html.xpath('//td[@class="nextpage"]/strong[2]/text()')[0])
        table = html.xpath('//table[@cellpadding="2"]')[0]
        for ii in table.iter('tr'):
            aa=ii.getchildren() #<td>
            try:
                bb = aa[0].getchildren()
                stock['sym'] = bb[0].text
                stock['name']=aa[1].text
                self.stocknameA.append(stock.copy())                
            except:
                pass

        
        urllist = (self.url_name % (i,) for i in range(51,npage*50,50))
        tmp = [self.parse_name(url,self.stocknameA) for url in urllist]
        # result = tostring(tablenews[0],encoding='utf8')
        
    def get_nameB(self):
        """
        just 2 pages, and no new B stock will be issued
        """
        stock = {} # name and symbol
        # extract the number of pages
        urllist = (self.urlb % (i,) for i in range(1,52,50))
        [self.parse_name(url,self.stocknameB) for url in urllist]
        
        
    def save_mongo(self):
        """ save stock name data to mongodb
        """
        [Stock(name=stock['name'],sym=stock['sym']+'.SS',
              goosym='SHA:'+stock['sym']).save() for stock in self.stocknameA]
        [Stock(name=stock['name'],sym=stock['sym']+'.SS',
              goosym='SHA:'+stock['sym']).save() for stock in self.stocknameB]
        
        
        
class USStock(object):
    """include nyse,nasdaq and amex
    """
    def __init__(self):
        areader = csv.reader(open('nasdaq.csv'))
        areader.next()
        [save_mongo(row) for row in areader]

    def save_mongo(self,row):
        Stock(sym=row[0], goosym='NASDAQ:'+row[0], name=row[1],
              sector=row[5],industry=row[6]).save()
        
    


