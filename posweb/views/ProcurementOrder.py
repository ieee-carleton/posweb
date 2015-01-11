from pyramid.response import Response
from decimal import *
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError
from time import strftime

from posweb.security import getUser

from posweb.models.shared import DBSession
from posweb.models.SaleItem import SaleItem, SaleItemCache

from posweb.models.OrderItem import Order, OrderLineItem
from posweb.models.ProcurementOrder import ProcurementOrder, ProcurementOrderItem
from pyramid.exceptions import NotFound 
from posweb.resources import (ApiRouter, Root)
def RequestIsAPI(context, request):
    if (context.__parent__ == ApiRouter):
        return True

    return False
def RequestIsPage(context, request):
    print context.__parent__
    if (context.__parent__ == Root):
        return True
    return False

@view_config(context='posweb.resources.SingleProcOrder', renderer='../templates/ProcOrder.jinja2', request_method='GET', custom_predicates=(RequestIsPage,), permission='inventory')
def GetProcOrder(request):
    print "serving request context:", request.context.__name__
    order = DBSession.query(ProcurementOrder).filter_by(id = request.context.__name__).first()
    if (order is None):
        return NotFound("No matching order found!")
    else:
            return {'order': order, 'logged_in': request.authenticated_userid}



@view_config(context='posweb.resources.NewProcOrder', renderer='../templates/new_proc_order.jinja2', request_method='GET', custom_predicates=(RequestIsPage,), permission='inventory')
def NewProcOrder(request):
    print "serving request context:", request.context.__name__
    if (request.context.__name__ == 'new'):
        return {'logged_in' : request.authenticated_userid}
    else:
        return NotFound('The system did not understand your request')



@view_config(context='posweb.resources.NewProcOrder', renderer='json', request_method='POST', custom_predicates=(RequestIsAPI,), permission='inventory')
def PostProcOrder(request):
    print "serving request context: ", request.context.__name__
    print "request", request
    if (request.json_body is None):
        return NotFound()

    ProcessErrorCode = 0

    currentTimeStamp = strftime("%Y-%m-%d %H:%M:%S")
    orderUser =getUser(request.json_body['fulfilledBy']) 
    
    if (orderUser is None):
        ProcessErrorCode = 9
    # convert to cents format

    order_total = int(Decimal(request.json_body['orderTotal']) * 100)
    temp_order = ProcurementOrder(orderUser, order_total)

    for item in request.json_body['items']:
        saleitem = DBSession.query(SaleItem).filter_by(id = item['id']).first()
        if (saleitem is None):
            ProcessErrorCode = 5
            break
        else:
            item_count = int(item['count'])
            temp_order.LineItems.append(ProcurementOrderItem(saleitem, item_count))
            if (saleitem.stockCount != -1):
                saleitem.stockCount = saleitem.stockCount + item_count; 
        DBSession.add(saleitem)
        

    if (ProcessErrorCode  == 0):
        temp_order.CommitDate = currentTimeStamp      
        DBSession.add(temp_order)

        committedOrder = DBSession.query(ProcurementOrder).filter_by(CommitDate=currentTimeStamp).one()
        print "committed transaction #", committedOrder.id
        return {'status': ProcessErrorCode,'redirect': request.application_url + '/app/procurements/' + str(committedOrder.id)}
    

    else:
        print "Process error code: ", ProcessErrorCode
        return {'status': ProcessErrorCode}

