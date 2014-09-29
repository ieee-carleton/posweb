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

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    Name = Column(Text)
    requiresPin = Column(Integer)
    Pin = Column(Text)
    ownerId = Column(Integer, ForeignKey('users.id'))
    currentTotal = Column(Integer)
    Orders = relationship('Order', lazy='dynamic',backref='account')
    Owner = relationship('User')

    def __init__(self, name, Owner, currentTotal, requirespin=False, Pin=""):
        self.Name = name
        self.Owner = Owner
        if (requirespin):
            self.requiresPin = 1
            self.Pin = Pin
        else:
            self.requiresPin = 0
            self.Pin = 0


        self.currentTotal = currentTotal

    def __json__(self):
        return {'id': self.id, 'name': self.Name , 'requiresPin': self.requiresPin, 'Owner': self.Owner.username}

