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

import datetime
from models import Meme, Image

def seed_data():
    fry_key = Image(name="fry_squint", image_file="fry.png").put()
    jc_key = Image(name="jackie_chan_wtf", image_file="jackie.png").put()
    tears_key = Image(name="tears_in_the_rain", image_file="tears.png").put()
    pika_key = Image(name="surprised_pikachu", image_file="surprised_pikachu.png").put()
    buzz_key = Image(name="buzz_everywhere", image_file="buzz_everywhere.jpg").put()
    roll_safe_key = Image(name="roll_safe", image_file="roll_safe.jpg").put()


    Meme(top_text="Not sure if meme app", bottom_text="or black hole",
         image=fry_key, creator="aprotim@gmail.com",
         created_at=datetime.datetime(2018, 07, 23, 05, 23, 0, 0)).put()
    Meme(top_text="Meme app", bottom_text="doesn't save memes?",
         image=jc_key, creator="aprotim@gmail.com",
         created_at=datetime.datetime(2018, 06, 23, 05, 23, 0, 0)).put()
    Meme(top_text="All these memes", bottom_text="lost like tears in the rain.",
         image=tears_key, creator="aprotim@gmail.com",
         created_at=datetime.datetime(1984, 07, 23, 05, 23, 0, 0)).put()
