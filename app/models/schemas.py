from marshmallow import fields

from app.models.models import Asset, Manager, Site
from config import db, ma


class ManagerSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Manager
        sqla_session = db.session
        load_instance = True

    sites = fields.Nested("ManagerSiteSchema", many=True)


class ManagerSiteSchema(ma.SQLAlchemyAutoSchema):
    """This class exists to get around a recursion issue"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    site_id = fields.Int()


class SiteSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Site
        sqla_session = db.session
        load_instance = True

    assets = fields.Nested("SiteAssetSchema", many=True)


class SiteAssetSchema(ma.SQLAlchemyAutoSchema):
    """This class exists to get around a recursion issue"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    asset_id = fields.Int()
    name = fields.Str()
    type = fields.Str()
    p_nominal = fields.Int()


# OPTIONALL
class AssetSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Asset
        sqla_session = db.session
        load_instance = True
