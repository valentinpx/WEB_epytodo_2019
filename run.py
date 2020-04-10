#!/usr/bin/env python3

try:
    from app import app
    app.run()
except:
    print("Failed to launch the app. Try to install required modules via:\npip3 install --no-cache-dir -r requirements.txt")
