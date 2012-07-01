import base64


class Session:

  def __init__(self, request=None):
    self.clear()
    if request != None:
      try:
        val = request.cookies["auth"]
        self.decode(val)
      except:
        pass

  def clear(self):
    self._id = None
    self._name = None
    self._expires = None
    self.valid = False

  def set(self, id, name, exp):
    self._id = id
    self._name = name
    self._expires = exp
    self._valid = True

  def encode(self):
    if self._valid == False:
      return ""

    val = str(self._id) + "," + self._name + "," + str(self._expires)
    val = base64.encodestring(val)

    return val

  def decode(self, value):
    if value == None:
      self.clear()
      return self._valid

    val = base64.decodestring(value)

    lst = val.split(",")
    #print lst
    self._id, self._name, self._expires = lst
    print "id=" + self._id + ",name=" + self._name + ",exp=" + self._expires

    self._valid = True
    return self._valid

  def get_name(self):
    if self._name != None:
      return self._name
    return ""

  def get_id(self):
    if self._id != None:
      return self._id
    return ""
