__author__ = 'Timur'

import uuid
from src.common.database import Database

#Python built-in datetime module
import _datetime

class Post(object):
    # _id is used to to be compatible to the ID that MongoDB gives by default
    # we want to overwrite MongoDB's default id with our id.
    def __init__(self, blog_id, title, content, author, created_date=_datetime.datetime.utcnow(), _id=None):
        #initialization method
        #date and id have been given default values

        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.created_date = created_date

        #to generate unique id
        # uuid is module
        # uuid4 is method to generate random id
        # hex is 32-bit character hexadecimal string
        # if an ID does not exist
        # Default value for id is None
        # Note: Default parameter has to be put at the end
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        #connect to Database class
        #save itself into JSON data type
        #save data into collection called 'posts'
        Database.insert(collection='posts',
                        data=self.json())

    def json(self):
        #create json representation (key-value pair)
        return{
            '_id': self._id,
            'blog_id': self.blog_id,
            'author': self.author,
            'content': self.content,
            'title': self.title,
            'created_date': self.created_date
        }

    '''first method: using static method
    @staticmethod
    def from_mongo(id):
        #returning mongoDB data; e.g. Post.from_mongo('123')
        return Database.find_one(collection='posts', query={'id': id})
    '''
    '''second method: using class method'''
    @classmethod
    def from_mongo(cls,id):
        post_data = Database.find_one(collection='posts', query={'_id': id})
        # return an object type Post
        ''' Before Argument Unpacking
        return cls(blog_id=post_data['blog_id'],
                   title=post_data['title'],
                   content=post_data['content'],
                   author=post_data['author'],
                   created_date=post_data['created_date'],
                   _id=post_data['_id'])
        '''
        # Argument unpacking allows us to pass a dictionary as parameters
        # to a method, by using the keys as parameter names, and the values
        # as parameter values
        return cls(**post_data)

    @staticmethod
    def from_blog(id):
        return [post for post in Database.find(collection='posts', query={'blog_id':id})]
