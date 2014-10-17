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
        admin_user = User(username='admin', password=bcrypt.hashpw('password', bcrypt.gensalt()), groups='admins')
        cash_account = Account("Cash", admin_user, 0, requirespin=False)
        if os.path.exists("items.list"):
            with open("items.list") as f:
                for line in f:
                    if line == "":
                        continue
                    elements = [x.strip() for x in line.split(',')]
                    print elements
                    item = SaleItem(int(elements[0]), elements[1], elements[2], int(elements[3]), 0)
    		if (len(elements) > 4):
    			item.stockCount = int(elements[4])
                DBSession.add(item)
        DBSession.add(admin_user)
        DBSession.add(cash_account)
