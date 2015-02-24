from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    ForeignKey
    )

from sqlalchemy.orm import relationship, backref
from posweb.models.SaleItem import SaleItem
from posweb.models.User import User

from shared import DBSession, Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    createdById = Column(Integer, ForeignKey('users.id'))
    commitDate = Column(Text)
    orderTotal = Column(Integer)
    toAccountId = Column(Integer, ForeignKey('accounts.id'))
    orderLineItems = relationship('OrderLineItem', lazy='dynamic')
    createdBy = relationship('User')


    def __init__(self, createdBy, commitDate, orderTotal):
        self.createdBy = createdBy
        self.commitDate = commitDate
        self.orderTotal = orderTotal

    def __json__(self, request):
        return {'id': self.id, 'createdBy': self.createdBy, 'commitDate': self.commitDate, 'orderTotal': self.orderTotal,
        'items' : [x.__json__() for x in self.orderLineItems]}



class DiscountCode(Base):
	__tablename__ = "discountCodes"
	id=Column(Integer, primary_key=True)
	isActive=Column(Integer)
	appliesTo=Column(Text)
	text=Column(Text)
	discountAmount=Column(Integer)
	
	def __init(self, isActive=true,appliesTo,text,amount):
		self.isActive = int(isActive)
		self.appliesTo = appliesTo
		self.text = text
		self.amount = amount


class OrderLineItem(Base):
    __tablename__ = "orderLineItem"
    id = Column(Integer, primary_key=True)
    sourceOrderId = Column(Integer, ForeignKey("orders.id"))
    itemId = Column(Integer, ForeignKey('saleItems.id'))
    count = Column(Integer)
    saleItem = relationship(SaleItem)
    
    
    def __init__(self, saleItem, count):
        self.saleItem = saleItem
        self.count = count


    def __json__(self):
        return {'item' : self.SaleItem.__json__(), 'count' : self.count}