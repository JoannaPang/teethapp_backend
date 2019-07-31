import os
import pymysql

CSRF_ENABLE = False
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}
]

#SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:buaa2019@localhost:3306/teethapp" #pang_comment
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost:3306/teethapp" #pang_add
SQLALCHEMY_COMMIT_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
