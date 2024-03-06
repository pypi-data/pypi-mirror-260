from flask import redirect, url_for, Blueprint, current_app
from sqlalchemy import MetaData, create_engine

base = Blueprint("base", __name__)

@base.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='img/favicon.png'), 308)

@base.route('/k8srad/liveness', methods=['GET'])
def liveness():
    return '', 200

@base.route('/k8srad/readiness', methods=['GET'])
def readiness():
    meta = MetaData(create_engine(current_app.config['SQLALCHEMY_DATABASE_URI']))
    meta.reflect(views=True)
    if 'ab_user' in meta.tables:
        return '', 200
    return '', 503