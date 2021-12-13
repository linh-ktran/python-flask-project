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
    name = fields.Str()
    address = fields.Str()
    p_max = fields.Int()


class SiteSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Site
        sqla_session = db.session
        load_instance = True

    manager = fields.Nested("SiteManagerSchema", default=None)
    assets = fields.Nested("SiteAssetSchema", many=True)


class SiteManagerSchema(ma.SQLAlchemyAutoSchema):
    """This class exists to get around a recursion issue"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    manager_id = fields.Int()
    lname = fields.Str()
    fname = fields.Str()


class SiteAssetSchema(ma.SQLAlchemyAutoSchema):
    """This class exists to get around a recursion issue"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    asset_id = fields.Int()
    name = fields.Str()
    type = fields.Str()
    p_nominal = fields.Int()


class AssetSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Asset
        sqla_session = db.session
        load_instance = True

    site = fields.Nested("AssetSiteSchema", default=None)


class AssetSiteSchema(ma.SQLAlchemyAutoSchema):
    """This class exists to get around a recursion issue"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    site_id = fields.Int()
    name = fields.Str()
    address = fields.Str()
    p_max = fields.Int()
