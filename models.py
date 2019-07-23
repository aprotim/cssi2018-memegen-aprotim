from google.appengine.ext import ndb

class Image(ndb.Model):
    name =  ndb.StringProperty(required=True)
    image_file =  ndb.StringProperty(required=True)

#One to One
class Meme(ndb.Model):
    top_text = ndb.StringProperty(required=False, default="")
    middle_text = ndb.StringProperty(required=False, default="")
    bottom_text = ndb.StringProperty(required=False, default="")
    image = ndb.KeyProperty(Image)
    creator = ndb.StringProperty(required=True)
    created_at = ndb.DateTimeProperty(required=True, auto_now_add=True)
