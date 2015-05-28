from google.appengine.ext import ndb

class Inputs (ndb.Model):
    input1 = ndb.StringProperty()
    input2 = ndb.StringProperty()
    input3 = ndb.StringProperty()
    nastanek = ndb.DateTimeProperty(auto_now_add=True)
    izbrisan = ndb.BooleanProperty(default=False)

