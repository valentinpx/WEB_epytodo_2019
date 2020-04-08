from flask import request, session
from app import app
from .controller import *

@app.route("/")
def hello_world():
    return ("<a href=\"https://www.youtube.com/watch?v=dQw4w9WgXcQ?t=1\">Hello, World!</a>")

@app.route("/register", methods=["POST"])
def register():
    return (register_user(session, request))

@app.route("/signin", methods=["POST"])
def signin():
    return (signin_user(session, request))

@app.route("/signout", methods=["POST"])
def signout():
    return (signout_user(session))

@app.route("/user", methods=["GET"])
def get_user():
    return (get_user_infos(session))

@app.route("/user/task", methods=["GET"])
def get_task():
    return (get_user_task(session))

@app.route("/user/task/<int:id>", methods=["GET", "POST"])
def update_task(id):
    return (modify_task(session, request, id))

@app.route("/user/task/add", methods=["POST"])
def add_task():
    return (new_task(session, request))

@app.route("/user/task/del/<int:id>", methods=["POST"])
def del_task(id):
    return (rm_task(session, id))
