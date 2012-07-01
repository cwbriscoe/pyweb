from Session import Session


class Auth:

  def __init__(self, conn):
    self._conn = conn

  def validate(self, name, pwd):
    cur = self._conn.cursor()

    cur.execute("""
      SELECT users.id   as id
            ,users.name as name
            ,auth.hash  as pass
        FROM users
            ,auth
       WHERE users.id   = auth.user_id
         and users.name = '""" + name + """'
         and auth.hash  = '""" + pwd + """'
    """)

    numrows = cur.rowcount
    assert numrows in {0, 1}

    if numrows == 0:
      return None

    row = cur.fetchone()
    sess = Session()
    sess.set(row[0], row[1], 9999)
    return sess

  def decode(self, value):
    if value == None:
      self.clear()
      return

    lst = value.split(",")
    #print lst
    self._id, self._name, self._expires = lst
    print "id=" + self._id + ",name=" + self._name + ",exp=" + self._expires
