from .models import User, Task
from flask import jsonify
from datetime import datetime
from hashlib import sha256

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


def register_user(session, request):
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

def signin_user(session, request):
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

def signout_user(session):
    if ("ID" in session):
        session.pop("ID", None)
        return ({"result" : "signout successful"})
    return (jsonify(None))


def get_user_infos(session):
    if (not "ID" in session):
        return ({"error" : "you must be logged in"})
    user = User.get_by_id(session["ID"])
    if (user is None):
        return ({"error" : "internal error"})
    return ({"result" : {"user_id" : user.user_id, "username" : user.username}})

def get_user_task(session):
    if (not "ID" in session):
        return ({"error" : "you must be logged in"})
    dest = []
    for task in User.get_by_id(session["ID"]).tasks:
        status = get_status(task.status)
        dest.append({task.task_id : {"title" : task.title, "begin" : format_t(task.begin), "end" : format_t(task.end), "status" : status}})
    return ({"result" : {"tasks" : dest}})


def modify_task(session, request, id):
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

def new_task(session, request):
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

def rm_task(session, id):
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