from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class no_autoflush(object):
    def __init__(self, session):
        self.session = session
        self.autoflush = session.autoflush

    def __enter__(self):
        self.session.autoflush = False

    def __exit__(self, type, value, traceback):
        self.session.autoflush = self.autoflush