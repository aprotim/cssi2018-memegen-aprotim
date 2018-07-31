#!/usr/bin/python
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import datetime
import json
import webapp2
import os
import jinja2
import random

import seed_memes

from models import Meme, Template
from google.appengine.api import users



#remember, you can get this by searching for jinja2 google app engine
jinja_current_directory = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MemeBrowser(webapp2.RequestHandler):
    def get(self):
        logout_link = users.create_logout_url('/')
        memes = Meme.query().order(-Meme.created_at).fetch(10)
        for meme in memes:
            meme.template_filename = meme.template.get().image_file
        start_template=jinja_current_directory.get_template("templates/latestmemes.html")
        self.response.write(start_template.render({'memes': memes, 'logout_link': logout_link}))

class AddMemeHandler(webapp2.RequestHandler):
    def get(self):
        logged_in_user = users.get_current_user()
        if logged_in_user:
            templates = Template.query().fetch()
            add_template=jinja_current_directory.get_template("templates/new_meme.html")
            self.response.write(add_template.render({'templates': templates}))
        else:
            login_prompt_template = jinja_current_directory.get_template('templates/login_please.html')
            self.response.write(login_prompt_template.render({'login_link': users.create_login_url('/')}))

    def post(self):
        user = users.get_current_user()
        template_name = self.request.get('template')
        template_key = Template.query(Template.name == template_name).fetch(1)[0].key
        Meme(top_text=self.request.get('top_text'),
             bottom_text=self.request.get('bottom_text'),
             template=template_key,
             creator=user.user_id(),
             created_at=datetime.datetime.utcnow()).put()
        self.redirect('/')

class UpdateMemeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.content_type = 'text/json'
        since = float(self.request.get('since'))
        since_dt = datetime.datetime.fromtimestamp(since)
        new_memes = Meme.query(Meme.created_at >= since_dt).order(-Meme.created_at).fetch()
        new_memes_list = []
        for meme in new_memes:
            template = meme.template.get()
            new_memes_list.append({
              'image_file': template.image_file,
              'top_text': meme.top_text,
              'bottom_text': meme.bottom_text,
            })
        self.response.write(json.dumps(new_memes_list))



class LoadDataHandler(webapp2.RequestHandler):
    def get(self):
        seed_memes.seed_data()

app = webapp2.WSGIApplication([
    ('/', MemeBrowser),
    ('/seed-data', LoadDataHandler),
    ('/add_meme', AddMemeHandler),
    ('/updated_memes', UpdateMemeHandler)
], debug=True)
