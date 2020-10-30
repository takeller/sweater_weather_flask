import os 

class Development(object):
    DEBUG = True

class Testing(object): 
    DEBUG = True
    TESTING = True

config = { 
    'development': Development, 
    'testing': Testing
}