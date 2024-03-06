import datetime
from sqlalchemy import Boolean
from sqlalchemy.orm import registry
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String


mapper_registry = registry()

class Version(Model):
    __tablename__ = 'k8srad_version'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False, unique=True)
    mayor = Column(Integer, nullable=False, unique=False)
    minor = Column(Integer, nullable=False, unique=False)
    patch = Column(Integer, nullable=False, unique=False)
    updated_at = Column(String(150), default=datetime.datetime.now().isoformat(), nullable=False)
    is_current = Column(Boolean, nullable=False, unique=False)
