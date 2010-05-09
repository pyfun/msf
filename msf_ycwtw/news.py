import urllib
from lxml.html import fromstring, tostring, open_in_browser
from lxml.html import builder as E

class ChinaNews(object):
    def __init__(self):
        """financeother includes 4,5,6,7,8,9,10 corresponding to
        bond, future, forex,hk_stock,options,index_future,longshort
        """
        url_fo = ['http://infofactory.newone.com.cn/zszq/pages/financeother/financeIndex.dhtml?menuId=%d&bkid=%d' % (i,i)
                  for i in range(4,11)]
        url = ['http://infofactory.newone.com.cn/zszq/pages/fund/financeIndex.dhtml?menuId=3&bkid=3', #fund
               'http://infofactory.newone.com.cn/zszq/pages/stock/financeIndex.dhtml?menuId=2&bkid=2', #stock
               'http://infofactory.newone.com.cn/zszq/pages/finance/financeIndex.dhtml?menuId=1&bkid=1']#home
        url_newone = url + url_fo

        newone_news = [self.parse_newone(ii) for ii in url_newone]
        self.build_newone(newone_news)

    def parse_newone(self,url):
        f = urllib.urlopen(url)
        data = f.read()
        f.close()
        # to unicode
        data = data.decode('utf-8')
 
        html = fromstring(data)
        html.make_links_absolute("http://infofactory.newone.com.cn")
        tablenews = html.xpath("//table[@cellpadding=4]")
        return tablenews[0]
        # result = tostring(tablenews[0],encoding='utf8')

    def build_newone(self,table):
#        html = E.HTML(E.HEAD(),E.BODY(table))
        head = """<html><body>"""
        foot = """</body></html>"""
        html = " ".join([tostring(i) for i in table])
        page = fromstring(head+html+foot)
        open_in_browser(page)
                      
if __name__ == '__main__':
    tmp = ChinaNews()
