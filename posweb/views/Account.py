from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from posweb.models.models import (
    DBSession,
    MyModel,
    )
from posweb.models.Account import Account

from posweb.resources import (ApiRouter, Root)
def RequestIsAPI(context, request):
    if (context.__parent__ == ApiRouter):
        return True

    return False
def RequestIsPage(context, request):
    if (context.__parent__ == Root):
        return True
    return False

@view_config(context='posweb.resources.AccountCollection', renderer='json', custom_predicates=(RequestIsAPI,), request_method='GET', permission='get_accounts')
def GetAccounts(request):
    print "Accounts requested!"
    try:
        items = DBSession().query(Account).all()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {"accounts" : items}

