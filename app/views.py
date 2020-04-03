from app import app

@app.route('/')
def hello_world():
    return ("<a href=\"https://www.youtube.com/watch?v=dQw4w9WgXcQ?t=1\">Hello, World!</a>")

@app.route('/register', methods=['POST'])
def register():
    return ("Work in progress")

@app.route('/signin', methods=['POST'])
def signin():
    return ("Work in progress")

@app.route('/signout', methods=['POST'])
def signout():
    return ("Work in progress")

@app.route('/user', methods=['GET'])
def get_user():
    return ("Work in progress")

@app.route('/user/task', methods=['GET'])
def get_task():
    return ("Work in progress")

@app.route('/user/task/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    return ("Work in progress")

@app.route('/user/task/add', methods=['POST'])
def add_task():
    return ("Work in progress")

@app.route('/user/task/del/<int:id>', methods=['POST'])
def del_task(id):
    return ("Work in progress")
