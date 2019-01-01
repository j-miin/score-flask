import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_login import LoginManager, current_user
import config 





app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


app.config.from_object(os.environ['APP_SETTINGS'])


db = SQLAlchemy(app)

Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

## API Routes ##


#import user model so that you can run migration
from score_keeping.users.models import User

from score_keeping.users.route import users_api_blueprint


app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/')

