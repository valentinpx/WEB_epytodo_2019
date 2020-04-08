#!/usr/bin/env python3

try:
    import flask
    import flask_sqlalchemy
except:
    print("Failed to import required modules. Try to run:\npip install --no-cache-dir -r requirements.txt")

from app import app

app.run()