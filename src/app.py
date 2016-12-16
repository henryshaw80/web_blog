__author__ = "Timur"

from flask import Flask, render_template, request, session
from src.models.user import User
from src.common.database import Database
from src.models.blog import Blog

# Blog, Post and User models
# Database class

# __name__ is built in variable in python
app = Flask(__name__)
# we set a secure secret key in flask when sending data
app.secret_key = "Timur"

# once program reach the end point '/'
@app.route('/') # 127.0.0.1:5000/
def home_template():
    return render_template('home.html')

# once program reach the end point '/login'
# it will run hello_method()
@app.route('/login') # 127.0.0.1:5000/login
def login_template():
    # we need to render jinja2 language into something
    # that a web browser understand
    return render_template('login.html')

# once program reach the end point '/register'
@app.route('/register') # 127.0.0.1:5000/register
def register_template():
    return render_template('register.html')

# since the program is trying to access a dictionary that is None
# we need initialize database before we request for a database
# we use Flask function called before_first_request to run
# initialize database method
@app.before_first_request
def initialize_database():
    Database.initialize()

# get the content of that form to get email and password
# method is only accepting POST request, alternative method is GET
@app.route('/auth/login', methods=['POST'])
# a login method once the '/login/' end point is reached.
def login_user():
    # website is going to make a request to an application
    email = request.form['email']
    password = request.form['password']
    # checking validity of the email
    if User.login_valid(email, password):
        User.login(email)
    else:
        # when email is not valid
        session['email'] = None

    # render template with data from application
    return render_template("profile.html", email=session['email'])

# Registration page
@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    User.register(email, password)
    # note that under register method, we have set
    # session['email'] = email

    # render template with data from application
    return render_template("profile.html", email=session['email'])

# Blogs list
@app.route('/blogs/<string:user_id>') # if we reach this route, user_id will be used
@app.route('/blogs/') #if we reach this route, user_id will be None, find using email
def user_blogs(user_id=None):
    if user_id is not None:
       # find user with his or her id
        user = User.get_by_id(user_id)
    else:
        # we are accessing own blog. that's why we query using email
        user = User.get_by_email(session['email'])

    # get his or her blogs
    blogs = user.get_blogs()

    # render blogs to display blogs list
    return render_template("user_blogs.html", blogs=blogs, email=user.email)

# Post lists, once user has access to his or her blog
@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()

    return render_template('post.html', posts=posts, blog_title=blog.title)

# if the process is equal to starting point, run the app
# if there are other process that already run
# the app, don't run the app
if __name__ == '__main__':
    app.run(port=5000)
