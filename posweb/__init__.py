from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from posweb.security import getGroups, getUserFromRequest

from posweb.models.shared import (
    DBSession,
    Base,
    )
from .resources import Root





def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    authentication_secret = settings['auth.secret']
    authn_policy = AuthTktAuthenticationPolicy(authentication_secret, callback=getGroups, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings, root_factory=Root)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.add_request_method(getUserFromRequest, 'user', reify=True)
    config.include('pyramid_chameleon')
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('login', '/login')
    config.add_route('home', '/')

    config.add_route('logout', '/logout')

    config.scan()
    Base.metadata.create_all()
    return config.make_wsgi_app()
