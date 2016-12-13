__author__ = 'Timur'

import uuid
import _datetime
from src.models.post import Post
from src.common.database import Database

class Blog(object):
    # _id is used to to be compatible to the ID that MongoDB gives by default
    # we want to overwrite MongoDB's default id with our id.
    def __init__(self, author, title, description, author_id, _id=None):
        self.author = author
        self.title = title
        self.description = description
        self.author_id = author_id
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_post(self, title, content, date=_datetime.datetime.utcnow()):
        '''
        # User will submit Title and Content in their website
        # using the user.py. We can remove some redundancies.
        title = input("Enter post title:")
        content = input("Enter post content:")
        date = input("Enter post date, or leave blank for today (in format DDMMYYYY):")

        Instead the method will receive the data as parameters through API.
        '''

        post = Post(blog_id=self._id,
                    title=title,
                    content=content,
                    author=self.author,
                    created_date=date)
        #strp: string parse time; to get string from formated date
        # %d = 2 digits for day, %m = 2 digits for month,
        # %Y = 4 digits for year

        post.save_to_mongo()

    def get_posts(self):
        return Post.from_blog(self._id)

    def save_to_mongo(self):
        #connect to Database class
        #save itself into JSON data type
        #save data into collection called 'blogs'
        Database.insert(collection='blogs',
                        data=self.json())

    def json(self):
        # create json representation (key-value pair)
        return {
            'author': self.author,
            'author_id': self.author_id,
            'title': self.title,
            'description': self.description,
            '_id': self._id
        }

    '''first method: using static method
    @staticmethod
    def get_from_mongo(id):
        blog_data = Database.find_one(collection='blogs',
                                      query={'id': id})

        #Instead of returning json data,
        #we want to return a Blog object contains data
        return Blog(author=blog_data['author'],
                    title=blog_data['title'],
                    description=blog_data['description'],
                    id=blog_data['id'])
    '''

    '''second method: using class method
    simplify things if the class name changes'''
    @classmethod
    def from_mongo(cls, id):
        blog_data = Database.find_one(collection='blogs',
                                  query={'_id': id})
        ''' Before Argument Unpacking
        return cls(author=blog_data['author'],
               title=blog_data['title'],
               description=blog_data['description'],
               _id=blog_data['_id'])
        '''
        # Argument unpacking allows us to pass a dictionary as parameters
        # to a method, by using the keys as parameter names, and the values
        # as parameter values
        return cls(**blog_data)

    '''search blog using author_id'''
    @classmethod
    def find_by_author_id(cls, author_id):
        # query the cursor because user need to list out their blogs
        blogs = Database.find(collection='blogs',
                                  query={'author_id': author_id})
        # return blog object of each blog in blogs list
        return [cls(**blog) for blog in blogs]
