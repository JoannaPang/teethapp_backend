from app import db
from config import SQLALCHEMY_DATABASE_URI

import os.path

db.create_all()