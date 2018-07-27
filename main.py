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
        memes = Meme.query().order(-Meme.created_at).fetch(10)
        for meme in memes:
            meme.template_filename = meme.template.get().image_file
        start_template=jinja_current_directory.get_template("templates/latestmemes.html")
        self.response.write(start_template.render({'memes': memes}))

class AddMemeHandler(webapp2.RequestHandler):
    def get(self):
        templates = Template.query().fetch()
        add_template=jinja_current_directory.get_template("templates/new_meme.html")
        self.response.write(add_template.render({'templates': templates}))

    def post(self):
        user = users.get_current_user()
        template_name = self.request.get('template')
        template_key = Template.query(Template.name == template_name).fetch(1)[0].key
        Meme(top_text=self.request.get('top_text'),
             bottom_text=self.request.get('bottom_text'),
             template=template_key,
             creator=user.email(),
             created_at=datetime.datetime.utcnow()).put()
        self.redirect('/')


class LoadDataHandler(webapp2.RequestHandler):
    def get(self):
        seed_memes.seed_data()

app = webapp2.WSGIApplication([
    ('/', MemeBrowser),
    ('/seed-data', LoadDataHandler),
    ('/add_meme', AddMemeHandler),
], debug=True)
