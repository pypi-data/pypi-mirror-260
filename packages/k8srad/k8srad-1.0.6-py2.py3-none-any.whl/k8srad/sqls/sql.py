import os

from flask import current_app
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from k8srad.models import Version


class Sqls:
    engine = None
    session = None
    folderPath = ""


    def __init__(self, app=None):
        if app is None:
            self.engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
        else:
            self.engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        self.session = scoped_session(sessionmaker(autocommit=False,
                                                   autoflush=False,
                                                   bind=self.engine))
        self.folderPath = os.path.dirname(os.path.abspath(__file__))

    def update_1_0_0(self):
        ma, mi, pa = 1, 0, 0
        if self.session.query(Version).count() == 0:
            self.setNewVersion(ma, mi, pa)


    def executeSQLScript(self, file_path):
        with self.engine.connect() as con:
            with open(file_path) as file:
                query = text(file.read())
                con.execute(query)

    def upgradeNeeded(self, mayor, minor, patch):
        curr_mayor, curr_minor, curr_patch = self.getCurrentVersion()
        if curr_mayor < mayor or curr_minor < minor or curr_patch < patch:
            return True
        return False

    def getCurrentVersion(self):
        current_version = self.session.query(Version).filter_by(is_current=True).first()
        return current_version.mayor, current_version.minor, current_version.patch

    def setNewVersion(self, mayor, minor, patch):
        curr_vers = self.session.query(Version).filter_by(is_current=True).all()
        for curr_ver in curr_vers:
            curr_ver.is_current = False
            self.session.commit()
        newVersion = Version(
            name="{}.{}.{}".format(mayor, minor, patch),
            mayor=mayor,
            minor=minor,
            patch=patch,
            is_current=True
        )
        self.session.add(newVersion)
        self.session.commit()


