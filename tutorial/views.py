from pyramid.view import view_config


@view_config(route_name='home', renderer='home.jinja2')
def my_view(request):
  '''
  print
  print
  print request
  print
  print
  print request.environ
  print
  print
  print request.environ['wsgi.multiprocess']
  '''
  return {'project': 'tutorial'}
