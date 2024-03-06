import os, logging
import sys
from datetime import timedelta
from waitress import serve
from dotenv import dotenv_values
from flask import Flask
from flask_appbuilder import SQLA, AppBuilder
from flask_session import Session
from werkzeug.middleware.proxy_fix import ProxyFix
from k8srad.views import VersionView
from k8srad.server import ServerAroParser
from k8srad.sqls.sql import Sqls
from k8srad.blueprint import base
from flask_appbuilder.security.manager import (
    AUTH_DB,
    AUTH_LDAP,
)

basedir = os.path.abspath(os.path.dirname(__file__))
# init Flask
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)
app.register_blueprint(base)

app.config.from_pyfile(basedir + "/config.py")
log_level = logging.INFO
if os.getenv("K8SRAD_CONF_FILE") is not None:
    dotenv_path = os.getenv("K8SRAD_CONF_FILE")
    if not os.path.isfile(dotenv_path):
        print("ERROR: Cannot find .env File in {path}. Cannot start.".format(path=dotenv_path))
        sys.exit(1)
    app.config.update(dotenv_values(dotenv_path))
    log_level = logging.DEBUG if app.config['K8SRAD_LOG_LEVEL'].upper() == "DEBUG" else log_level
    log_level = logging.WARNING if app.config['K8SRAD_LOG_LEVEL'].upper() == "WARNING" else log_level
    log_level = logging.FATAL if app.config['K8SRAD_LOG_LEVEL'].upper() == "FATAL" else log_level
    log_level = logging.INFO if app.config['K8SRAD_LOG_LEVEL'].upper() == "INFO" else log_level
    log_level = logging.ERROR if app.config['K8SRAD_LOG_LEVEL'].upper() == "ERROR" else log_level

logging.getLogger().setLevel(log_level)
log_format = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"

if 'K8SRAD_LOG_FILE' in app.config:
    try:
        with open(app.config['K8SRAD_LOG_FILE'], 'w') as f:
            f.write('K8SRAD Logfile')
        logging.basicConfig(filename=app.config['K8SRAD_LOG_FILE'], format=log_format)
    except FileNotFoundError as e:
        print("Cannot create log file. Stop processing. Error: {error}".format(error=e))
        sys.exit(1)
else:
    logging.basicConfig(format=log_format)

app.logger.info("The APP is running in {LOGLEVEL} mode.".format(LOGLEVEL=logging.getLevelName(log_level)))

if "K8SRAD_APP_NAME" in app.config:
    app.config["APP_NAME"] = app.config["K8SRAD_APP_NAME"]
app.logger.info("Starting K8SRAD with name {APP_NAME}.".format(APP_NAME=app.config["APP_NAME"]))

if "K8SRAD_APP_ICON" in app.config:
    app.config["APP_ICON"] = app.config["K8SRAD_APP_ICON"]
app.logger.info("Adding {APP_ICON} as App icon.".format(APP_ICON=app.config["APP_ICON"]))

app.config["AUTH_TYPE"] = AUTH_DB
if app.config["K8SRAD_AUTH_TYPE"] == "ldap":
    app.config["AUTH_TYPE"] = AUTH_LDAP

app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=10)
if "K8SRAD_SESSION_LIFETIME" in app.config:
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(seconds=int(app.config["K8SRAD_SESSION_LIFETIME"]))

# Init Database for Server Sessions
server_session = Session(app)
server_session.app.session_interface.db.create_all()

db = SQLA(app)
db.create_all()

# Init Appbuilder Authentication and Authorization
appbuilder = AppBuilder(app, db.session)
appbuilder.add_view(VersionView, "Versions", category="Security", icon="fa-list")
admin = appbuilder.sm.find_user(username="admin")

# Setup default Database
if admin == None:
    role_admin = appbuilder.sm.find_role(
        appbuilder.sm.auth_role_admin
    )
    admin = appbuilder.sm.add_user(
        username="admin",
        first_name="admin",
        last_name="admin",
        email="info@yotron.de",
        role=role_admin,
        password="admin"
    )
    db.session.add(admin)
    db.session.commit()

# Init and Migrate
sqls = Sqls(app)
sqls.update_1_0_0()


def run():
    argParser = ServerAroParser()
    args = argParser.parser.parse_args()
    serve(app, **argParser.getKw(args))
