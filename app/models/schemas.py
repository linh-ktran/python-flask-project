"""Marshmallow schemas for request/response validation."""

from marshmallow import Schema, fields, validate

from app.models.models import AssetType


# -- Requests --

class ManagerCreateSchema(Schema):
    first_name = fields.String(required=True, validate=validate.Length(min=1, max=80))
    last_name = fields.String(required=True, validate=validate.Length(min=1, max=80))
    site_ids = fields.List(fields.Integer(), load_default=[])


class ManagerUpdateSchema(Schema):
    first_name = fields.String(validate=validate.Length(min=1, max=80))
    last_name = fields.String(validate=validate.Length(min=1, max=80))
    site_ids = fields.List(fields.Integer())


class SiteCreateSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=120))
    address = fields.String(required=True, validate=validate.Length(min=1, max=250))
    max_power = fields.Integer(required=True, validate=validate.Range(min=0))
    manager_ids = fields.List(fields.Integer(), load_default=[])


class SiteUpdateSchema(Schema):
    name = fields.String(validate=validate.Length(min=1, max=120))
    address = fields.String(validate=validate.Length(min=1, max=250))
    max_power = fields.Integer(validate=validate.Range(min=0))
    manager_ids = fields.List(fields.Integer())


class AssetCreateSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=120))
    asset_type = fields.String(required=True, validate=validate.OneOf(AssetType.ALL))
    nominal_power = fields.Integer(required=True, validate=validate.Range(min=1))


class AssetUpdateSchema(Schema):
    name = fields.String(validate=validate.Length(min=1, max=120))
    asset_type = fields.String(validate=validate.OneOf(AssetType.ALL))
    nominal_power = fields.Integer(validate=validate.Range(min=1))


# -- Responses --

class AssetResponseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    asset_type = fields.String()
    nominal_power = fields.Integer()
    site_id = fields.Integer()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class SiteSummarySchema(Schema):
    """Short version for nesting inside manager responses."""
    id = fields.Integer()
    name = fields.String()


class ManagerSummarySchema(Schema):
    """Short version for nesting inside site responses."""
    id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()


class ManagerResponseSchema(Schema):
    id = fields.Integer(dump_only=True)
    first_name = fields.String()
    last_name = fields.String()
    sites = fields.List(fields.Nested(SiteSummarySchema))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class SiteResponseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    address = fields.String()
    max_power = fields.Integer()
    total_power = fields.Integer(dump_only=True)
    available_power = fields.Integer(dump_only=True)
    assets = fields.List(fields.Nested(AssetResponseSchema))
    managers = fields.List(fields.Nested(ManagerSummarySchema))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class MessageSchema(Schema):
    message = fields.String()
