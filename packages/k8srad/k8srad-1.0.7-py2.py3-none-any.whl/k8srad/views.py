import datetime

from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView

from k8srad.models import Version


class VersionView(ModelView):
    route_base = '/versions'
    datamodel = SQLAInterface(Version)
    list_columns = [
        'name',
        'mayor',
        'minor',
        'patch',
        'updated_at',
        'is_current'
    ]
    edit_columns = [
        'name'
    ]