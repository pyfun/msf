from mongoengine import *
import datetime

connect('stock',host='18.47.5.206')

class Stock(Document):
    sym = StringField(primary_key=True) #yahoo symbol: 601988.SS
    name = StringField(max_length=50)
    goosym = StringField(max_length=20) # google style: SHA:601988
    bsymid = StringField(max_length=50) # bloomberg open bsym unique id
    province = StringField(max_length=20) # sheng fen or state
    sector = StringField(max_length=50)
    industry = StringField(max_length=50)            

    meta = {
        'indexes': ['sym']
        }

    def __unicode__(self):
        return self.sym

"""
Day, month and week price will use almost the same
Five minute price, the OHLC will be a list for every day
"""
class PriceDay(Document):
    sym = StringField(primary_key=True) #yahoo symbol plus date, unique: 601988.SS.19990401
    o = FloatField(min_value=0.0)
    h = FloatField(min_value=0.0)
    l = FloatField(min_value=0.0)
    c = FloatField(min_value=0.0)
    v = FloatField(min_value=0.0)
    a = FloatField(min_value=0.0)

    meta = {
        'indexes':['-sym']
        }

    def __unicode__(self):
        return self.sym 

class PriceWeek(Document):
    sym = StringField(primary_key=True) #yahoo symbol plus date, unique: 601988.SS.19990401
    o = FloatField(min_value=0.0)
    h = FloatField(min_value=0.0)
    l = FloatField(min_value=0.0)
    c = FloatField(min_value=0.0)
    v = FloatField(min_value=0.0)
    a = FloatField(min_value=0.0)

    meta = {
        'indexes':['-sym']
        }

    def __unicode__(self):
        return self.sym 
    

class PriceMonth(Document):
    sym = StringField(primary_key=True) #yahoo symbol plus date, unique: 601988.SS.19990401
    o = FloatField(min_value=0.0)
    h = FloatField(min_value=0.0)
    l = FloatField(min_value=0.0)
    c = FloatField(min_value=0.0)
    v = FloatField(min_value=0.0)
    a = FloatField(min_value=0.0)

    meta = {
        'indexes':['-sym']
        }

    def __unicode__(self):
        return self.sym 
    

class PriceMin(Document):
    sym = StringField(primary_key=True) #yahoo symbol plus date, unique: 601988.SS.199904010930
    o = ListField(FloatField(min_value=0.0))
    h = ListField(FloatField(min_value=0.0))
    l = ListField(FloatField(min_value=0.0))
    c = ListField(FloatField(min_value=0.0))
    v = ListField(FloatField(min_value=0.0)) 
    a = ListField(FloatField(min_value=0.0))

    meta = {
        'indexes':['-sym']
        }

    def __unicode__(self):
        return self.sym 
