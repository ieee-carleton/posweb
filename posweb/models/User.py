from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    )

from shared import DBSession, Base


class User(Base):
    @property
    def __acl__(self):
        return [
            (Allow, self.username, 'view_user'),
        ]

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(Text)
    fullname = Column(Text)
    email = Column(Text)
    password = Column(Text)
    groups = Column(Text)

    def __init__(self, **kwargs):
        if 'username' in kwargs:
            self.username = kwargs['username']
        if 'password' in kwargs:
            self.password = kwargs['password']
        if 'groups' in kwargs:
            self.groups = kwargs['groups']
    
    def getGroupList(self):
        return [x.strip() for x in self.groups.split(',')]