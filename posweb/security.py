from posweb.models.shared import DBSession
from posweb.models.User import User
from pyramid.security import unauthenticated_userid

from sqlalchemy.exc import DBAPIError
import bcrypt
def getGroups(userid, request):
    user = request.user
    if user is not None:
        return user.getGroupList()
    return None

def authenticateUser(userid, password):
    print "authenticating user " + userid
    try:
        user = DBSession().query(User).filter_by(username = userid).first()
    except DBAPIError as err:
        print "Error connecting to the database!"
        print err
        return False
    if (user is None):
        return False
    return (bcrypt.hashpw(password.encode('ascii', 'ignore') ,user.password.encode('ascii', 'ignore')) == user.password)


def getUser(userid):
    print "userid is ", userid
    try:
        user = DBSession().query(User).filter_by(username = userid).first()
    except DBAPIError as err:
        print err
        print "Error connecting to the database!"
        return None
    if (user is None):
        print "Warning: NoneUser returned"
    return user

def getUserFromRequest(request):
    userid = unauthenticated_userid(request)
    return getUser(userid)