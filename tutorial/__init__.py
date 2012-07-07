import os
import logging
import psycopg2 as dbase
from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.events import subscriber
from pyramid.events import ApplicationCreated
from pyramid.request import Request
from classes.Session import Session


#setup logging
logging.basicConfig()
log = logging.getLogger(__file__)
here = os.path.dirname(os.path.abspath(__file__))


class MyRequest(Request):
  def __init__(self, environ):
    if hasattr(Request, '__init__'):
      Request.__init__(self, environ)
    #pass
    self.sess = Session(self)


@subscriber(ApplicationCreated)
def application_created_subscriber(event):
  log.warn('Initializing application...')


@subscriber(NewRequest)
def new_request_subscriber(event):
  #log.warn('new request')
  request = event.request
  settings = request.registry.settings
  request.db = dbase.connect(settings['dsn'])
  request.add_finished_callback(close_db_connection)


def close_db_connection(request):
  request.db.close()


def main(global_config, **settings):
  #print settings
  config = Configurator(settings=settings)

  config.set_request_factory(MyRequest)

  #configure jinja2
  config.include('pyramid_jinja2')
  #config.add_jinja2_extension('compressinja.html.HtmlCompressor')
  config.add_jinja2_search_path("tutorial:templates")
  jinja = config.get_jinja2_environment()
  jinja.trim_blocks = True

  config.add_static_view('static', 'static', cache_max_age=3600)
  #config.override_asset(to_override='favicon.icon', override_with='/static/favicon.ico')
  config.add_route('favicon', '/favicon.ico')
  config.add_route('home', '/')
  config.add_route('login', '/login')
  config.scan()
  return config.make_wsgi_app()
