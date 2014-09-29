from pyramid.response import Response
from pyramid.view import view_config
from pyramid.security import has_permission, ACLAllowed
from decimal import *


from sqlalchemy.exc import DBAPIError

from posweb.models.models import (
    DBSession,
    MyModel,
    )
from posweb.models.SaleItem import SaleItem

from posweb.resources import (ApiRouter, Root)
def RequestIsAPI(context, request):
    if (context.__parent__ == ApiRouter):
        return True

    return False
def RequestIsPage(context, request):
    if (context.__parent__ == Root):
        return True
    return False

@view_config(context='posweb.resources.ItemCollection', renderer='json', custom_predicates=(RequestIsAPI,), request_method='GET')
@view_config(context='posweb:resources.ItemCollection', renderer='../templates/ItemsList.jinja2', custom_predicates=((RequestIsPage,)),request_method='GET')
def GetSaleItems(request):
    print "SaleItems requested!"
    can_create = False
    try:
        items = DBSession().query(SaleItem).all()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    print has_permission("create_items", request.context, request)
    if (isinstance(has_permission("create_items", request.context, request),ACLAllowed)):
        print "Can create new items: true"
        can_create = True

    return {"items" : items, "can_create": can_create}

@view_config(context='posweb.resources.NewItem', renderer='json', request_method='POST', custom_predicates=(RequestIsAPI,), permission='create_item')
def PostNewItem(request):
    print "serving request context", request.context.__name__
    try:
        item_name = request.json_body['plainName']
        item_id = int(request.json_body['id'])
        d = Decimal(request.json_body['value']) * 100;
        item_value = int(d)
        item_category = request.json_body['category']
        item = SaleItem(item_category, item_name, item_value, 0)
        item.id = item_id
        DBSession.add(item)

        return {'status': 0}
    except:
        return {'status': 1}





@view_config(context='posweb.resources.SingleItem', renderer='json', request_method='GET', custom_predicates=(RequestIsAPI,))
def GetSaleItem(request):
    print "serving request context:", request.context.__name__
    try:
        item = DBSession.query(SaleItem).filter_by(id = request.context.__name__).first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'item' : item}

