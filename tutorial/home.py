from pyramid.view import view_config
from classes.Session import Session


@view_config(route_name='home', renderer='home.jinja2')
def home_view(request):
  title = 'Home Page'

  sess = Session(request)

  print "home page view now running, name=" + sess.get_name()

  cur = request.db.cursor()
  cur.execute("""
    SELECT users.name as name
          ,auth.hash  as pass
      FROM users
          ,auth
     WHERE users.id = auth.user_id;
   """)
  rows = cur.fetchall()

  return {'title': title, 'sess': sess, 'rows': rows}
