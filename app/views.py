from app import app

@app.route('/')
def hello_world():
    return ("<a href=\"https://www.youtube.com/watch?v=dQw4w9WgXcQ?t=1\">Hello, World!</a>")