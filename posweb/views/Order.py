from pyramid.response import Response
from pyramid.view import view_config
import transaction
from sqlalchemy.exc import DBAPIError
from time import strftime

from posweb.security import getUser

from posweb.models.shared import DBSession
from posweb.models.SaleItem import SaleItem, SaleItemCache

from posweb.models.OrderItem import Order, OrderLineItem
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

@view_config(context='posweb.resources.SingleOrder', renderer='../templates/Order.jinja2', request_method='GET', custom_predicates=(RequestIsPage,), permission='new_order')
def GetOrder(request):
    print "serving request context:", request.context.__name__
    order = DBSession.query(Order).filter_by(id = request.context.__name__).first()
    if (order is None):
        return NotFound("No matching order found!")
    else:
            return {'order': order, 'logged_in': request.authenticated_userid}



@view_config(context='posweb.resources.NewOrder', renderer='../templates/new_order.jinja2', request_method='GET', custom_predicates=(RequestIsPage,), permission='new_order')
def NewOrder(request):
    print "serving request context:", request.context.__name__
    if (request.context.__name__ == 'new'):
        return {'logged_in' : request.authenticated_userid}
    else:
        return NotFound('The system did not understand your request')



@view_config(context='posweb.resources.NewOrder', renderer='json', request_method='POST', custom_predicates=(RequestIsAPI,), permission='new_order')
def PostOrder(request):
    print "serving request context: ", request.context.__name__
    if (request.json_body is None):
        return NotFound()
    try:    
        # we're doing the total ourselves, don't trust the client
        currentTotal = 0
        ProcessErrorCode = 0
        redirect = ""
        currentTimeStamp = strftime("%Y-%m-%d %H:%M:%S")
        temp_order = Order(getUser(request.authenticated_userid), currentTimeStamp, 0)
        for item in request.json_body['items']:
            saleitem = DBSession.query(SaleItem).filter_by(id = item['id']).first().autoflush(False)     
            if (saleitem is None):
                ProcessErrorCode = 5
                break

            else:
                item_count = int(item['count'])
                temp_order.orderLineItems.append(OrderLineItem(saleitem, item_count ))
                currentTotal += int(item['count']) * saleitem.value

                if (saleitem.stockCount != -1):
                    if ((saleitem.stockCount - item_count) < 0):
                        ProcessErrorCode = 4
                        raise Exception("Item out of stock!")

                    else:
                        saleitem.stockCount = saleitem.stockCount - item_count

        temp_order.orderTotal = currentTotal
        
        if (ProcessErrorCode == 0):
            print "adding to session"           
            DBSession.add(temp_order)
            committedOrder = DBSession.query(Order).filter_by(commitDate=currentTimeStamp).one()
            print "committed transaction #", committedOrder.id
            redirect = request.application_url + '/app/orders/' + str(committedOrder.id)
    except Exception as e:
        print e
        transaction.rollback()
        DBSession.expunge()
    finally:
        print "Process error code: ", ProcessErrorCode
        return {'status': ProcessErrorCode, 'redirect': redirect}

