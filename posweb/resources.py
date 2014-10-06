from pyramid.security import (
    Allow,
    Everyone,
    ALL_PERMISSIONS
    )
from .security import getUser
from posweb.models.User import User
class Root(object):
	__name__= ''
	__parent__ = None
	__acl__ = [ (Allow, Everyone, 'view_orders'),
				(Allow, Everyone, 'get_saleItems'),
				(Allow, 'execs', ('make_accounts, open_accounts', 'new_procurement', "create_item")),
                (Allow, 'volunteers', ('new_order', 'get_accounts')),
                (Allow, 'admins', ALL_PERMISSIONS) ]

	def __init__(self, request):
		pass
	
	def __getitem__(self, key):
		if (key=='api'):
			return ApiRouter(Root)
		elif (key == 'app'):
			return URLRouter(Root)
		
		

class URLRouter(object):
	__name__= ''
	__parent__= Root

	def __init__(self, parent=Root):
		self.__parent__ = parent

	def __getitem__(self, key):
		if(key == 'items'):
			return ItemCollection(self.__parent__)
		elif(key == 'orders'):
			return OrderCollection(self.__parent__)
		elif(key == 'accounts'):
			return AccountCollection(self.__parent__)
		elif(key == 'users'):
			return UserCollection(self.__parent__)
		elif(key == 'procurements'):
			return ProcurementCollection(self.__parent__)
		raise KeyError





class UserCollection(object):
	__name__ = ''
	__parent__ = Root
	def __init__(self, parent=Root):
		self.__parent__= parent

	def __getitem__(self, key):
		if key == 'new':
			user = User()
			user.__parent__ = self.__parent__
			user.__name__ = key
			su = SingleUser(key, self.__parent__)
			su.user = user
			return su
		else:
			print "retrieving user ", key
			user = getUser(key)
			user.__parent__ = self.__parent__
			user.__name__ = key
			su = SingleUser(key, self.__parent__)
			su.user = user
			return su
		raise KeyError


class SingleUser(object):
	@property
	def __acl__(self):
		return [(Allow, self.user.username, 'view_user'),]

	def __init__(self, name, parent=Root):
		self.__name__ = name
		self.__parent__ = parent


class ApiRouter(URLRouter):
	def __init__(self, parent):
		URLRouter.__init__(self,ApiRouter)
	def __getitem__(self, key):
		print "API request received!"
		return URLRouter.__getitem__(self, key)
	

class ItemCollection(object):
	__name__ = ''
	__parent__ = Root

	def __init__(self, parent=Root):
		self.__parent__ = parent

	def __getitem__(self, key):
		if (key != "new"):
			return SingleItem(key, self.__parent__)
		elif (key =="new"):
			return NewItem(key, self.__parent__)

class NewItem(object):
	def __init__(self, name, parent=Root):
		self.__name__ = name
		self.__parent__ = parent	


class SingleItem(object):
	def __init__(self, name, parent=Root):
		self.__name__ = name
		self.__parent__ = parent


class OrderCollection(object):
	__name__ = ''
	__parent__=Root

	def __init__(self, parent=Root):
		self.__parent__ = parent

	
	def __getitem__(self, key):
		if (key == 'new'):
			return NewOrder(key, self.__parent__)
		else:
			return SingleOrder(key, self.__parent__)


class ProcurementCollection(object):
	__name__ = ''
	__parent__=Root

	def __init__(self, parent=Root):
		self.__parent__ = parent

	
	def __getitem__(self, key):
		print "new proc requested!"
		if (key == 'new'):
			return NewProcOrder(key, self.__parent__)
		else:
			return SingleProcOrder(key, self.__parent__)

class SingleOrder(object):
	def __init__(self, name, parent=Root):
		self.__name__ = name
		self.__parent__ = parent

class NewOrder(object):
	def __init__(self, name, parent=Root):
		self.__name__ = name
		self.__parent__ = parent


class AccountCollection(object):
	__name__ = ''
	__parent__=Root

	def __init__(self, parent=Root):
		self.__parent__ = parent

	
	def __getitem__(self, key):
		if (key == 'new'):
			return NewAccount(key, self.__parent__)
		else:
			return SingleAccount(key, self.__parent__)

class SingleAccount(object):
	def __init__(self, name, parent=Root):
		self.__name__ = name
		self.__parent__ = parent

class NewAccount(object):
	def __init__(self, name, parent=Root):
		self.__name__ = name
		self.__parent__ = parent



class SingleProcOrder(object):
	
	def __init__(self, name, parent=Root):
		self.__name__ = name
		self.__parent__ = parent

class NewProcOrder(object):
	def __init__(self, name, parent=Root):
		self.__name__ = name
		self.__parent__ = parent

