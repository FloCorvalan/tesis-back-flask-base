from flask import Flask, request, Response, jsonify
from functools import wraps
from database import database

# blueprint import
#from apps.jenkins.views import jenkins_app
from .login.login import login
from .models.users import users
from .models.team import team
from .models.developer import developer
from .models.source import source
from .models.team_project import team_project
from .pm.views import pm
from .process_model.views import process_model
from .participation.views import participation
from .prod.views import prod
from .models.user import User
from flask_cors import CORS
from bson import json_util
from datetime import datetime, timedelta
import os


def create_app(config):
    app = Flask(__name__)
    # app.secret_key = b'9Jx#\xdd\x0f1\xf4\xa6\x8f\t\x97\x14\x1dh\xe6'
    CORS(app, supports_credentials=True)
    # setup with the configuration provided
    app.config.from_object(config)
    app.config["SESSION_TYPE"] = "filesystem"
    #app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

    # setup all our dependencies
    mongo = database.init_app(app)

    # register blueprint
    app.register_blueprint(login)
    app.register_blueprint(users)
    app.register_blueprint(team, url_prefix='/team')
    app.register_blueprint(developer, url_prefix='/developer')
    app.register_blueprint(source, url_prefix='/source')
    app.register_blueprint(team_project, url_prefix='/team-project')
    app.register_blueprint(pm)
    app.register_blueprint(process_model, url_prefix='/process-model')
    app.register_blueprint(prod, url_prefix='/prod')
    app.register_blueprint(participation, url_prefix='/participation')
    #app.register_blueprint(app2, url_prefix="/app2")

    return app, mongo