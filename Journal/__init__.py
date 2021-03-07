import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager



app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'
app.config['WHOOSH_BASE'] = 'whoosh'

#################################
#### DATABASE SETUPS ############
################################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)



'''
with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        Migrate(app,db, render_as_batch=True)
    else:
'''
Migrate(app, db)

###########################
#### LOGIN CONFIGS #######
#########################

login_manager = LoginManager()

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.


from Journal.users.views import users
from Journal.core.views import core

app.register_blueprint(users)
app.register_blueprint(core)

login_manager.login_view = "users.login"

#login_manager.login_message = "Login Required to access home page"


