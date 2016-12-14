import uuid

import _datetime
from flask import session
from src.common.database import Database
from src.models.blog import Blog

__author__ = 'Timur'

class User(object):

    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls, email):
        # in the parameter there is no self, because
        # there is not necessarily exist a user object.
        # We use email to find user.
        data = Database.find_one("users", {"email": email})
        if data is not None:
            return cls(**data)
        '''
        # By default a method return NONE,
        # so we don't need to write
        return None
        '''
    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("users", {"_id": _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        # Check whether a user's email matches the password they sent us
        # e.g. user.login_valid ("hipstercamper@gmail.com", "1234")
        user = User.get_by_email(email)
        if user is not None:
            # Check the password with the input parameter password
            # if found, return True
            return user.password == password
        return False

    ''' # first method: using static method
    @staticmethod
    def register(email, password):
        # if the user already exist, return False
        user = User.get_by_email(email)
        if user is None:
            # User doesn't exist, create a new one
            new_user = User(email, password)
            new_user.save_to_mongo()
        else:
            # User exists
            return False
    '''

    # second method: using class method
    # to make it easier, if we decide to change class name
    @classmethod
    def register(cls, email, password):
        # if the user already exist, return False
        user = cls.get_by_email(email)
        if user is None:
            new_user = cls(email, password)
            new_user.save_to_mongo()

            # we save the e-mail to session during registration
            # to make the user log in. Fortunately, Flask
            # does the cookies for us. Flask re-sent them a cookie
            # that is unique secure and identifies with their session
            session['email'] = email

            # default is to return None
            # However, a better way is to
            return True
        else:
            return False

    # Usual method is to store user's e-mail to web browser cookie,
    # which will send such cookie (information) back to user.
    # To secure the user's identity, the user's email should be stored
    # in the server, which then send unique identifier for the session.
    # When User access the profile, User will send Unique identifier
    # and the program will identify the identifier and search the email
    # associated with the unique identifier in the cookie.
    # A session is like a cookie but stored on Server side.
    # Session have expiry time (e.g. 1 hour).

    @staticmethod
    def login(user_email):
        # Login_valid has already been called (i.e. user has a valid
        # email and password). Next time user ask for a profile,
        # They will send identifier in their cookie, which will be
        # able to identify the session that will store the e-mail.
        # if the session has no e-mail, the session has not been
        # logged in.
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    def get_blogs(self):
        # Return a Blog object that list all blogs of one
        # particular author_id associated with user._id
        return Blog.find_by_author_id(self._id)

    def new_blog(self, title, description):
        # author, title, description, author_id
        # the author and author_id can be completed since the program
        # knows the user (i.e. author) when they logged-in
        blog = Blog(author=self.email,
                    title=title,
                    description=description,
                    author_id=self._id)

        blog.save_to_mongo()

    @staticmethod
    def new_post(blog_id, title, content, date=_datetime.datetime.utcnow()):
        # title, content, date=_datetime.datetime.utcnow()
        blog = Blog.from_mongo(blog_id)
        blog.new_post(title=title,
                      content=content,
                      date=date)

    def json(self):
        # create json representation (key-value pair)
        return {
            'email': self.email,
            '_id': self._id,
            # sending password over network is never safe
            # However, in our case password is only being
            # passed inside the network
            'password': self.password
        }

    def save_to_mongo(self):
        Database.insert(collection='users',
                        data=self.json())
