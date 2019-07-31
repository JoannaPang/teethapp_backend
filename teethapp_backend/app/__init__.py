from flask import Flask
import pymysql
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os
#from .infer import getgraph #pang_comment_20190619
import logging
from .inference_softmax import create_model #pang_add_20190619

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

print('create_modeling...')
model = create_model()
print('create_model success!')

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
basedir = os.path.abspath(os.path.dirname(__file__))

from app import views, models
