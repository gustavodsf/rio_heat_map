#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Start our application."""

from flask import g
from flask_babel import Babel
import threading
from api.src.config.create_app import create_app
from api.src.data_crawler import DataCrawler
from tweets_grabber import TweetsGrabber

dataCrawler = DataCrawler()

def getData():
  threading.Timer(120.0, getData).start()
  dataCrawler.getData()

tweetsGrabber = TweetsGrabber()
tweetsGrabber.start()
getData()

app = create_app()
babel = Babel(app)
app.run(**app.config.get_namespace('RUN_'))


@babel.timezoneselector
def get_timezone():
    """Set the user timezone on babel."""
    user = g.get('user', None)
    if user is not None:
        return user.timezone
