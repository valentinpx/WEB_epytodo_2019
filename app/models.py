from app import db
from hashlib import sha256
from datetime import datetime

user_has_task = db.Table('user_has_task',
    db.Column('fk_user_id', db.Integer, db.ForeignKey('user.user_id')),
    db.Column('fk_task_id', db.Integer, db.ForeignKey('task.task_id')))

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column("user_id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(256))
    password = db.Column("password", db.String(256))
    tasks = db.relationship("Task", secondary=user_has_task)

    def __init__(self, username):
        self.username = username

    @staticmethod
    def get_by_name(name):
        return (User.query.filter_by(username=name).first())
    
    @staticmethod
    def get_by_id(id):
        return (User.query.get(id))

    def add(self, password):
        if (User.get_by_name(self.username) != None):
            return (False)
        self.password = str(sha256(str(password).encode('utf-8')).digest())
        db.session.add(self)
        db.session.commit()
        return (True)

    def has_task(self, task_id):
        for user_task in self.tasks:
            if (user_task.task_id == task_id):
                return (True)
        return (False)

class Task(db.Model):
    __tablename__ = "task"
    task_id = db.Column("task_id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(256))
    begin = db.Column("begin", db.DateTime, default=datetime.now())
    end = db.Column("end", db.DateTime, default=None)
    status = db.Column("status", db.Integer, default=0)

    def __init__(self, title):
        self.title = title
    
    @staticmethod
    def get_by_id(id):
        return (Task.query.get(id))

    def add(self, id, request):
        if ("begin" in request.form):
            self.begin = request["begin"]
        if ("end" in request.form):
            self.end = request["end"]
            if (self.end < self.begin):
                self.end = None
        if ("status" in request.form):
            if (request.form["status"] == "not started"):
                self.status = 0
            if (request.form["status"] == "in progress"):
                self.status = 1
            if (request.form["status"] == "done"):
                self.status = 2
        db.session.add(self)
        db.session.commit()

        user = User.get_by_id(id)
        user.tasks.append(self)
        db.session.add(user)
        db.session.commit()
        return (True)

    def update(self, request):
        if ("title" in request.form):
            self.title = request.form["title"]
        if ("begin" in request.form):
            self.begin = request.form["begin"]
        if ("end" in request.form):
            self.end = request.form["end"]
            if (self.end < self.begin):
                self.end = None
        if ("status" in request.form):
            self.status = request.form["status"]
        db.session.add(self)
        db.session.commit()

    def delete(self):
        id = self.task_id
        db.session.delete(self)
        db.session.commit()
        db.engine.execute("DELETE FROM user_has_task WHERE `fk_task_id`=" + str(id) + ";")