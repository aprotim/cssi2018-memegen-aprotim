#!/usr/bin/python

import json
import webapp2
import os
import jinja2

import seed_memes

from models import Meme, Image
from google.appengine.api import users
from google.appengine.ext import ndb



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
        start_template=jinja_current_directory.get_template("templates/latestmemes.html")
        self.response.write(start_template.render({'memes': memes,
                'latest_meme': latest_meme_key}))

# Handles new meme creation
class AddMemeHandler(webapp2.RequestHandler):
    def get(self):
        images = Image.query().fetch()
        add_template=jinja_current_directory.get_template("templates/new_meme.html")
        self.response.write(add_template.render({'images': images}))

    def post(self):
        user = users.get_current_user()
        image_name = self.request.get('image')
        image_key = Image.query(Image.name == image_name).fetch(1)[0].key
        Meme(top_text=self.request.get('top_text'),
             middle_text=self.request.get('middle_text'),
             bottom_text=self.request.get('bottom_text'),
             image=image_key,
             creator=user.user_id()).put()
        self.redirect('/')

# JSON endpoint for auto-refresh
class UpdateMemeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.content_type = 'text/json'
        if self.request.get('after'):
            latest_meme_key = ndb.Key(urlsafe=self.request.get('after'))
            latest_meme = latest_meme_key.get()
            new_memes = Meme.query(Meme.created_at > latest_meme.created_at).order(-Meme.created_at).fetch()
        else:
            new_memes = Meme.query().order(-Meme.created_at).fetch(10)
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
    ('/updated_memes', UpdateMemeHandler)
#    ('/notifier', NotificationHandler)
], debug=True)
