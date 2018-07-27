from google.appengine.ext import ndb

class Template(ndb.Model):
    name =  ndb.StringProperty(required=True)
    image_file =  ndb.StringProperty(required=True)

#One to One
class Meme(ndb.Model):
    top_text = ndb.StringProperty(required=False)
    bottom_text = ndb.StringProperty(required=False)
    template = ndb.KeyProperty(Template)
    creator = ndb.StringProperty(required=True)
    created_at = ndb.DateTimeProperty(required=True)
