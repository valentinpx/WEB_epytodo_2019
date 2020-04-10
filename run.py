#!/usr/bin/env python3

try:
    import flask
    import flask_sqlalchemy
    from app import app
    app.run()
except:
    print("Failed to import required modules. Try to run:\npip3 install --no-cache-dir -r requirements.txt")
