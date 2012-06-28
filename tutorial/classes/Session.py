class Session:

  def __init__(self, value=None):
    self.decode(value)

  def clear(self):
    self._id = None
    self._name = None
    self._expires = None
    self.valid = False

  def decode(self, value):
    if value == None:
      self.clear()
      return

    lst = value.split(",")
    #print lst
    self._id, self._name, self._expires = lst
    print "id=" + self._id + ",name=" + self._name + ",exp=" + self._expires
