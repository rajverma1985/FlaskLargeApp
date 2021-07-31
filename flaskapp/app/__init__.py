from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel, lazy_gettext as _l
import os
import config

basedir = os.path.abspath(os.path.dirname(__file__))

# as the app instance is not yet created initializing empty extensions(create global extension instances)
db = SQLAlchemy()
babel = Babel()  # used for translation
login_manager = LoginManager()


# using application factory:
def create_app(config_env=""):
    app = Flask(__name__)
    if not config_env:
        config_env = app.env  # setting the config env "FLASK_ENV" for app in case env is not set
    app.config.from_object("config.{}Config".format(config_env.capitalize()))
    # Initializing extensions, each flask extension provides and init method
    db.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.session_protection = "strong"
    login_manager.login_message = _l("you need to be logged in")
    login_manager.login_message_category = "danger"
    # Imports from subpackages (views)
    with app.app_context():
        from app.main.views import main
        app.register_blueprint(main)
    from app.auth.views import auth
    app.register_blueprint(auth)
    from app.unit1.views import unit1
    app.register_blueprint(unit1, url_prefix="/unit1")
    from app.unit2.views import unit2
    app.register_blueprint(unit2, url_prefix="/unit2")
    from app.main.views import page_not_found
    app.register_error_handler(404, page_not_found)
    return app
