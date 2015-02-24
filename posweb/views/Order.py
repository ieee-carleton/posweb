from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError
from time import strftime

from posweb.security import getUser

from posweb.models.shared import DBSession
from posweb.models.SaleItem import SaleItem, SaleItemCache

from posweb.models.OrderItem import Order, OrderLineItem
from pyramid.exceptions import NotFound 

from posweb.exceptions import InvalidItemError, ItemLookupError

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

    # we're doing the total ourselves, don't trust the client
    currentTotal = 0
    ProcessErrorCode = 0
    outOfStockItems = []
    message  = ""
    redirect = ""
    currentTimeStamp = strftime("%Y-%m-%d %H:%M:%S")
	discountcode = None
	discountItemSet = set()
    try:
        temp_order = Order(getUser(request.authenticated_userid), currentTimeStamp, 0)
        orderItems = [item['id'] for item in request.json_body['items']]
        orderSaleItems = list(DBSession.query(SaleItem).filter(SaleItem.id.in_(orderItems)).all())
		
		if 'discountcode' in request.json_body:
			code = request.json_body['discountcode'].lower()
			discountcode = DBSession.query(DiscountCode).filter(text = code).first()
			if (discountcode is None):
				raise DiscountCodeError(code)
				
			for (applicableItem in discountcode.appliesTo.split(",")):
				discountItemSet.add(int(applicableItem.strip()))
		
        if len(orderSaleItems) != len(orderItems):
            raise ItemLookupError("Something in the lookup process went wrong!")

        if None in orderSaleItems:
            raise InvalidItemError()

        orderItems =[item for item in request.json_body['items']]
        orderItems.sort(key=lambda x: x['id'])

        orderSaleItems.sort(key=lambda item: item.id)

        zippedItems = zip(orderSaleItems, orderItems)        
        #import pdb;  pdb.set_trace()
        for item in zippedItems:
            saleitem = item[0]
            discountAmount = 0
			temp_order.orderLineItems.append(OrderLineItem(saleitem,int(item[1]['count'])))
			if (saleitem.id in discountItemSet):
				discountAmount = discountcode.discountAmount;
            currentTotal += int(item[1]['count']) * (saleitem.value - discountAmount)

            if (saleitem.nonStockableItem != 1):
                if (saleitem.stockCount < int(item[1]['count'])):
                    ProcessErrorCode = 1
                    outOfStockItems.append(saleitem.id)
                saleitem.stockCount = saleitem.stockCount - int(item[1]['count'])

        temp_order.orderTotal = currentTotal
		
        DBSession.add(temp_order)
        DBSession.flush()
        print "committed transaction #", temp_order.id
        redirect = request.application_url + '/app/orders/' + str(temp_order.id)
        if (ProcessErrorCode  == 1):
            message ="Items (" + ','.join([str(n) for n in outOfStockItems]) + ") were marked as out of stock. Please contact the restocking director"
	except Error as e:
		print(e.message)
		ProcessErrorCode = e.id
		message = e.message
	
    except Exception as e:
        print "Invalid Operation"
        ProcessErrorCode = -6
        redirect = ''
        message = e.message
    finally:
        return {'status': ProcessErrorCode, 'redirect': redirect, 'message': message}

