import os
from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_login import LoginManager, current_user
import config
from score_keeping.helpers.uploader import uploader


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


app.config.from_object(os.environ['APP_SETTINGS'])


db = SQLAlchemy(app)

Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

## API Routes ##


# import user model so that you can run migration
from score_keeping.users.models import User
from score_keeping.users.route import users_api_blueprint


app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/')


@app.route("/api/v1/images/upload", methods=["POST"])
def upload():
    data = request.get_json(force=True)
    image_data = data.get("image")
    image_id = uploader(image_data)
    return make_response(jsonify({'public_id': image_id}))
