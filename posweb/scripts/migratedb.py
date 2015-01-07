#!/usr/bin/python
"""
Migration script for dbase to transition from legacy tracking mode
"""
import os
import sys
import transaction
import bcrypt
from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.shared import (
    DBSession,
    Base,
    )
from ..models.SaleItem import SaleItem
from ..models.User import User
from ..models.Account import Account


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    
    Base.metadata.create_all(engine)
    
    with transaction.manager:
        for saleItem in DBSession.query(SaleItem).all():
            if (saleItem.stockCount == -1):
                saleItem.nonStockableItem = 1
                saleItem.stockCount = 0
        
        #DBSession.add(admin_user)
        #DBSession.add(cash_account)



    
