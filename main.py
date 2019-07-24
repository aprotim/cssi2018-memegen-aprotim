#!/usr/bin/python

import json
import webapp2
import os
import jinja2

import seed_memes

from models import Meme, Image
from google.appengine.api import users
from google.appengine.ext import ndb

def get_meme_from_key(meme_key):
    meme_key_string = meme_key
    meme_key = ndb.Key(urlsafe=meme_key_string)
    return meme_key.get()

#remember, you can get this by searching for jinja2 google app engine
jinja_current_directory = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


# Displays all recent memes
class MemeBrowser(webapp2.RequestHandler):
    def get(self):
        memes = Meme.query().order(-Meme.created_at).fetch(10)
        if memes:
            latest_meme_key = memes[0].key.urlsafe()
        else:
            latest_meme_key = ""
        for meme in memes:
            meme.image_filename = meme.image.get().image_file
        start_template=jinja_current_directory.get_template(
            "templates/latestmemes.html")
        self.response.write(start_template.render({'memes': memes,
            'latest_meme': latest_meme_key}))

class ViewMemeHandler(webapp2.RequestHandler):
    def get(self):
        meme = get_meme_from_key(self.request.get('meme_key'))
        meme.image_filename = meme.image.get().image_file
        template=jinja_current_directory.get_template("templates/singlememe.html")
        self.response.write(template.render({'meme': meme}))


# Handles new meme creation
class AddMemeHandler(webapp2.RequestHandler):
    def get(self):
        images = Image.query().fetch()
        add_template=jinja_current_directory.get_template("templates/new_meme.html")
        self.response.write(add_template.render({'images': images}))


# Actually stores the memes to datastore
class SaveMemeHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user() # get current logged in user
        meme_key_string = self.request.get('meme_key')
        image_name = self.request.get('image')
        image_key = Image.query(Image.name == image_name).fetch(1)[0].key # get the key of the correct image by nickname

        if meme_key_string:
            meme = get_meme_from_key(meme_key_string)
            if meme.creator != user.user_id():
                self.response.status = "403 Forbidden"
                return
        else:
            meme = Meme()

        meme.top_text=self.request.get('top_text')
        meme.middle_text=self.request.get('middle_text')
        meme.bottom_text=self.request.get('bottom_text')
        meme.image=image_key
        meme.creator=user.user_id() # grab the user ID from currently logged in user, store with Meme

        meme_key = meme.put()
        self.redirect('/view?meme_key=' + meme_key.urlsafe())


# Like the Add handler, above, but lets you change an existing memes
class EditMemeHandler(webapp2.RequestHandler):
    def get(self):
        template_vars = {
            "images": Image.query().fetch(),
            "meme_key": self.request.get("meme_key")}
        meme = get_meme_from_key(self.request.get("meme_key"))
        template_vars["top_text"] = meme.top_text
        template_vars["middle_text"] = meme.middle_text
        template_vars["bottom_text"] = meme.bottom_text
        template_vars["image_name"] = meme.image.get().name
        add_template=jinja_current_directory.get_template("templates/new_meme.html")
        self.response.write(add_template.render(template_vars))


# JSON endpoint for auto-refresh
class RefreshMemesHandler(webapp2.RequestHandler):
    def get(self):
        self.response.content_type = 'text/json'
        if self.request.get('after'):
            latest_meme_key = ndb.Key(urlsafe=self.request.get('after'))
            latest_meme = latest_meme_key.get()
            new_meme_query = Meme.query(Meme.created_at > latest_meme.created_at).order(-Meme.created_at)
        else:
            new_meme_query = Meme.query().order(-Meme.created_at)
        user_id = self.request.get('after')
        if user_id:
            new_meme_query = new_meme_query.filter(Meme.creator == user_id)

        new_memes = new_meme_query.fetch()
        new_memes_list = []
        for meme in new_memes:
            image = meme.image.get()
            new_memes_list.append({
              'image_file': image.image_file,
              'top_text': meme.top_text,
              'middle_text': meme.middle_text,
              'bottom_text': meme.bottom_text,
              'created_at': meme.created_at.isoformat(),
              'key': meme.key.urlsafe(),
            })
        self.response.write(json.dumps(new_memes_list))


# For adding data
class LoadDataHandler(webapp2.RequestHandler):
    def get(self):
        seed_memes.seed_data()

app = webapp2.WSGIApplication([
    ('/', MemeBrowser),
    ('/seed-data', LoadDataHandler),
    ('/add_meme', AddMemeHandler),
    ('/updated_memes', RefreshMemesHandler),
    ('/view', ViewMemeHandler),
    ('/edit', EditMemeHandler),
    ('/save', SaveMemeHandler),
], debug=True)
