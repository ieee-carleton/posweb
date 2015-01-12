
from posweb.security import authenticateUser
from pyramid.view import (
    view_config,
    forbidden_view_config,
    )

from pyramid.security import (
    remember,
    forget,
    )
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPForbidden
from pyramid.security import authenticated_userid

@forbidden_view_config()
def forbidden_view(request):
# do not allow a user to login if they are already logged in
    if authenticated_userid(request):
        return HTTPForbidden()
    loc = request.route_url('login', _query=(('next', request.path),))
    return HTTPFound(location=loc)


@view_config(route_name='login', renderer='../templates/login.jinja2')
def login(request):
    login_url = request.route_url('login')
    next = request.params.get('next') or request.route_url('home')
    message = ''
    login = ''
    password = ''
    print "Tried to access:", next
    if 'form.submitted' in request.params:
        print "Login request submitted"
        login = request.params['login']
        password = request.params['password']
        if (authenticateUser(login, password)):
            headers = remember(request, login)
            print "Successfully authenticated %s" % login 
            return HTTPFound(location = next,
                             headers = headers)
        message = 'Failed login'

    return {
        'message' : message,
        'next' : next,
        'login' : login,
        'password' : password,
        }

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = request.route_url('home'),
                     headers = headers)
