from pyramid.view import (view_config)


@view_config(route_name='home', renderer='../templates/home.jinja2')
def NewOrder(request):
    d = {'login_url': request.application_url}
    if (request.authenticated_userid):
        d['logged_in'] = True
    return  d
