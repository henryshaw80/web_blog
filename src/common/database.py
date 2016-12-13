__author__ = "Timur"

import pymongo

class Database(object):
    #This class a definition of an object
    #with extra properties and actions
    #class Database will inherit from object

    #Universal Resource Identifier (URI)
    #static property
    #this is a class URI redides indide Database class
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    #all object will have the same URI and Database
    #hence, there is no need for Initialization
    #for URI nor Database, since we are only
    #using one database via one URI

    #since we won't be using self
    #we need to put a static method declaration
    #to let python know that self won't be used
    #because this method only belongs to Database class
    #not to an instance of a Database
    @staticmethod
    def initialize():
        #the URI lives inside Database
        client = pymongo.MongoClient(Database.URI)
        #accessing database called 'local'
        Database.DATABASE = client['local']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    '''
    A find query returns a cursor, this is essentially a
    no-operation scenario, as no actual data is returned
    (only the cursor information). If you call findOne,
    then you are actually returning the data and closing the cursor.
    '''
    #return a cursor
    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    #get the first element (JSON) object that cursor points
    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)