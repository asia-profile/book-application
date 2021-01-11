from flask import Flask
import logging
from flask import jsonify
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app);

#handles all migrateon
#migrate = Migrate(app, db)
migrate = Migrate(app, db, render_as_batch=True)

admin = Admin(app,template_mode='bootstrap3')

csrf = CSRFProtect(app)

#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(filename ='record.lg', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

from app import views, models
