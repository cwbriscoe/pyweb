from pyramid.view import view_config


@view_config(route_name='login', renderer='login.jinja2')
def login_view(request):
  title = 'Login Page'

  cur = request.db.cursor()
  cur.execute("""
    SELECT users.name as name
          ,auth.hash  as pass
      FROM users
          ,auth
     WHERE users.id = auth.user_id;
   """)
  rows = cur.fetchall()

  name = request.params['username']
  pwd = request.params['password']

  print "username:" + name + "    password:" + pwd

  return {'title': title, 'username': name, 'password': pwd}
