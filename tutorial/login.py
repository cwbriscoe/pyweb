import sys
from pyramid.view import view_config
from classes.Auth import Auth


@view_config(route_name='login', renderer='login.jinja2')
def login_view(request):
  title = 'Login Page'

  try:
    name = request.params['username']
    pwd = request.params['password']
  except KeyError:
    name = ""
    pwd = ""
  except:
    print "Unexpected error:", sys.exc_info()[0]
    raise

  #print "username:" + name + "    password:" + pwd

  if name != "":
    auth = Auth(request.db)
    sess = auth.validate(name, pwd)
    if sess != None:
      cookie = sess.encode()
      response = request.response
      response.set_cookie("auth", cookie, max_age=(7 * 24 * 60 * 60))
      print "Success! - " + cookie
    else:
      request.response.delete_cookie("auth")

  #debug
  try:
    c = request.cookies["auth"]
    debug = c
  except KeyError:
    debug = "Youareawhore"
  except:
    print "Unexpected error:", sys.exc_info()[0]
    raise

  return {'title': title, 'debug': debug, 'username': name, 'password': pwd}
