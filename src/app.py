__author__ = "Timur"

from flask import Flask, render_template

# Blog, Post and User models
# Database class

# __name__ is built in variable in python
app = Flask(__name__)

# once program reach the end point '/'
# it will run hello_method()
@app.route('/') # www.mysite.com/api/
def hello_method():
    # return "Hello, world!"
    # we need to render jinja2 language into something
    # that a web browser understand
    return render_template('login.html')

# if the process is equal to starting point, run the app
# if there are other process that already run
# the app, don't run the app
if __name__ == '__main__':
    app.run(port=5000)
