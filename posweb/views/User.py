
import bcrypt

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from posweb.models.shared import (
    DBSession
    )
from posweb.models.User import User
from posweb.security import getUser

from posweb.resources import (ApiRouter, Root)
def RequestIsAPI(context, request):
    if (context.__parent__ == ApiRouter):
        return True

    return False
def RequestIsPage(context, request):
    if (context.__parent__ == Root):
        return True
    return False

@view_config(context='posweb.resources.SingleUser', renderer='../templates/User.jinja2', permission='view_user')
def login(request):
    
    user = request.context.user
    userIsAdmin = 'admins' in getUser(request.authenticated_userid).getGroupList()
    print "userIsAdmin:", userIsAdmin
    id = user.id
    if 'form.submitted' in request.params:
        print request.params
        user.fullname = request.params['fullname']
        user.email = request.params['email']
        if 'changepw' in request.params:
            user.password = bcrypt.hashpw(request.params['password'].strip().encode('ascii', 'ignore'), bcrypt.gensalt())
        if ('admins' in getUser(request.authenticated_userid).getGroupList()):
            user.username = request.params['username']
            user.groups = request.params['groups']
        DBSession.add(user)
        if (user.id is None):
            user = DBSession.query(User).filter_by(id = request.params['username']).first()
        else:
            user = DBSession.query(User).filter_by(id = id).first()

    rd = {'user': user, 'logged_in' : request.authenticated_userid}
    if (userIsAdmin == True):
        rd['userIsAdmin'] = 'yes'
    return rd
