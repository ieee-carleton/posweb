from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    ForeignKey
    )

from sqlalchemy.orm import relationship, backref
from posweb.models.OrderItem import Order
from posweb.models.User import User

from shared import DBSession, Base

class ProcurementOrder(Base):
    __tablename__ = "procurementOrders"
    id = Column(Integer, primary_key=True)
    procuredById = Column(Integer, ForeignKey('users.id'))
    ReceiptTotal = Column(Integer)
    CommitDate = Column(Text)
    ReimbursementReference = Column(Text)
    FulfilledBy = relationship('User',uselist=False)
    LineItems = relationship('ProcurementOrderItem', lazy='dynamic')


    def __init__(self, user, rxTotal):
        self.ReceiptTotal = rxTotal
        self.FulfilledBy = user

class ProcurementOrderItem(Base):
    __tablename__ = "procurementOrderLineItems"
    id = Column(Integer, primary_key=True)
    procurementOrdId = Column(Integer, ForeignKey('procurementOrders.id'))
    saleItemId = Column(Integer, ForeignKey('saleItems.id'))
    procurementCount = Column(Integer)
    SaleItem = relationship('SaleItem',uselist=False)

    def __init__(self, item, count):
        self.SaleItem = item
        self.procurementCount = count

