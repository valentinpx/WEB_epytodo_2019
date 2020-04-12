from flask import request, session, render_template
import jinja2
from app import app
from .controller import *

# interactions with bdd

@app.route('/', methods=['GET'])
def view_index():
    return render_template('index.html')

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

# interactions with templates

@app.route('/login', methods=['GET'])
def view_login():
    return render_template('login.html')


@app.route('/register', methods=['GET'])
def view_register():
    return render_template('register.html')


@app.route('/home', methods=['GET'])
def view_home():
    if ("ID" in session):
        return render_template('home.html')
    return render_template('login-redirect.html')


@app.route('/add', methods=['GET'])
def view_add():
    if ("ID" in session):
        return render_template('add.html')
    return render_template('login-redirect.html')


@app.route('/edit/<id>', methods=['GET'])
def view_edit(id):
    if ("ID" in session):
        return render_template('edit.html')
    return render_template('login-redirect.html')
