
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


@view_config(route_name='login', renderer='../templates/login.jinja2')
@forbidden_view_config(renderer='../templates/login.jinja2')
def login(request):
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    print "came from:", came_from
    if 'form.submitted' in request.params:
        print "Logged in!"
        login = request.params['login']
        password = request.params['password']
        if (authenticateUser(login, password)):
            headers = remember(request, login)
            if (came_from == '/'):
                came_from = request.application_url + '/app/orders/new'
            return HTTPFound(location = came_from,
                             headers = headers)
        message = 'Failed login'

    return dict(
        message = message,
        url = request.application_url + '/login',
        came_from = came_from,
        login = login,
        password = password,
        )

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = request.route_url('login'),
                     headers = headers)
