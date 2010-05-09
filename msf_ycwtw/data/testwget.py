from time import time
import urllib
import subprocess

target = "http://market.finance.sina.com.cn/downxls.php?date=2010-04-22&symbol=sz000671"

wget_start = time()

proc = subprocess.Popen(["wget", target])
proc.communicate()

wget_end = time()


url_start = time()
a=urllib.urlretrieve(target,'test.csv')
print a
url_end = time()

print "wget -> %s" % (wget_end - wget_start)
print "urllib.urlretrieve -> %s"  % (url_end - url_start)

