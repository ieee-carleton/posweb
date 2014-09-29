from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    )

from shared import DBSession, Base
class SaleItemCache(object):
    def __init__(self):
        self.dCache = {}

    def __getitem__(self, key):
        pass


class SaleItem(Base):
    __tablename__ = "saleItems"
    id = Column(Integer, primary_key=True)
    category = Column(Text)
    plainName = Column(Text)
    value = Column(Integer)
    stockCount = Column(Integer)

    def __init__(self, category, name, val, stockCount):
    	self.category = category
    	self.plainName = name
    	self.value = val
    	self.stockCount = stockCount
        
    def __init__(self, sku, category, name, val, stockCount):
        self.id = sku
        self.category = category
        self.plainName = name
        self.value = val
        self.stockCount = stockCount

    

    def __json__(self, request):
        return {'id': self.id, 'category': self.category, 'plainName': self.plainName, 'value': self.value, 'stockCount': self.stockCount}




