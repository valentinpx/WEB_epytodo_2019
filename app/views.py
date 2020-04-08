from flask import request, jsonify, session
from hashlib import sha256
from app import app
from .models import User, Task
from datetime import datetime

def format_t(time):
    if (time != None):
        return (time.strftime("%Y-%m-%d %H:%M:%S"))
    return (None)

def get_status(nb):
    status = "not started"
    if (nb == 1):
        status = "in progress"
    if (nb == 2):
        status = "done"
    return (status)

@app.route("/")
def hello_world():
    return ("<a href=\"https://www.youtube.com/watch?v=dQw4w9WgXcQ?t=1\">Hello, World!</a>")

@app.route("/register", methods=["POST"])
def register():
    try:
        user = User(request.form["username"])
        if ("ID" in session):
            dest = {"error" : "internal error"}
        elif (user.add(request.form["password"]) == False):
            dest = {"error" : "account already exists"}
        else:
            dest = {"result" : "account created"}
    except:
        dest = {"error" : "internal error"}
    return (dest)

@app.route("/signin", methods=["POST"])
def signin():
    try:
        user = User.get_by_name(request.form["username"])
        if ("ID" in session):
            dest = {"error" : "internal error"}
        elif (user == None or
        str(sha256(str(request.form["password"]).encode("utf-8")).digest()) != user.password):
            dest = {"error" : "login or password does not match"}
        else:
            session["ID"] = user.user_id
            dest = {"result" : "signin successful"}
    except:
        dest = {"error" : "internal error"}
    return (dest)

@app.route("/signout", methods=["POST"])
def signout():
    if ("ID" in session):
        session.pop("ID", None)
        return ({"result" : "signout successful"})
    return (jsonify(None))

@app.route("/user", methods=["GET"])
def get_user():
    if (not "ID" in session):
        return ({"error" : "you must be logged in"})
    user = User.get_by_id(session["ID"])
    if (user is None):
        return ({"error" : "internal error"})
    return ({"result" : {"user_id" : user.user_id, "username" : user.username}})

@app.route("/user/task", methods=["GET"])
def get_task():
    if (not "ID" in session):
        return ({"error" : "you must be logged in"})
    dest = []
    for task in User.get_by_id(session["ID"]).tasks:
        status = get_status(task.status)
        dest.append({task.task_id : {"title" : task.title, "begin" : format_t(task.begin), "end" : format_t(task.end), "status" : status}})
    return ({"result" : {"tasks" : dest}})

@app.route("/user/task/<int:id>", methods=["GET", "POST"])
def update_task(id):
    if (not "ID" in session):
        return ({"error" : "you must be logged in"})
    user = User.get_by_id(session["ID"])
    task = Task.get_by_id(id)
    if (task == None):
        return ({"error" : "task id does not exist"})
    if (user.has_task(task.task_id) == False):
        return ({"error" : "internal error"})
    
    if (request.method == "GET"):
        return ({"result" : {"title" : task.title, "begin" : format_t(task.begin), "end" : format_t(task.end), "status" : get_status(task.status)}})
    try:
        task.update(request)
        dest = {"result" : "update done"}
    except:
        dest = {"error" : "internal error"}
    return (dest)

@app.route("/user/task/add", methods=["POST"])
def add_task():
    try:
        if (not "ID" in session):
            dest = {"error" : "you must be logged in"}
        else:
            task = Task(request.form["title"])
            task.add(session["ID"], request)
            dest = {"result" : "new task added"}
    except:
        dest = {"error" : "internal error"}
    return (dest)

@app.route("/user/task/del/<int:id>", methods=["POST"])
def del_task(id):
    if (not "ID" in session):
        return ({"error" : "you must be logged in"})
    user = User.get_by_id(session["ID"])
    task = Task.get_by_id(id)
    if (task == None):
        return ({"error" : "task id does not exist"})
    if (user.has_task(task.task_id) == False):
        return ({"error" : "internal error"})
    task.delete()
    return ({"result" : "task deleted"})
