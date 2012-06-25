import os
import logging
from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.events import subscriber
from pyramid.events import ApplicationCreated
import psycopg2 as dbase


#setup logging
logging.basicConfig()
log = logging.getLogger(__file__)
here = os.path.dirname(os.path.abspath(__file__))


'''
try:
  conn = dbase.connect("host='localhost' dbname='testdb' user='chris' password='commode'")
  print "Database connected"
except:
  print "I am unable to connect to the database"
'''

'''
try:
  cur = conn.cursor()
  cur.execute("""
    CREATE TABLE distributors (
      did     integer,
      name    varchar(40),
      PRIMARY KEY(did)
  );""")
  conn.commit()
except:
  print "Unable to create table"
'''


@subscriber(ApplicationCreated)
def application_created_subscriber(event):
    log.warn('Initializing application...')


@subscriber(NewRequest)
def new_request_subscriber(event):
    log.warn('new request')
    request = event.request
    settings = request.registry.settings
    request.db = dbase.connect(settings['dsn'])
    #request.db = dbase.connect("host='localhost' dbname='testdb' user='chris' password='commode'")
    #request.db = sqlite3.connect(settings['db'])
    request.add_finished_callback(close_db_connection)


def close_db_connection(request):
    request.db.close()


def main(global_config, **settings):
  #print settings
  config = Configurator(settings=settings)

  #configure jinja2
  config.include('pyramid_jinja2')
  #config.add_jinja2_extension('compressinja.html.HtmlCompressor')
  config.add_jinja2_search_path("tutorial:templates")
  jinja = config.get_jinja2_environment()
  jinja.trim_blocks = True

  config.add_static_view('static', 'static', cache_max_age=3600)
  config.add_route('home', '/')
  config.scan()
  return config.make_wsgi_app()
