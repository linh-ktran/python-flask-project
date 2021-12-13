"""This is the asset module and supports all the REST actions for the asset data"""
from typing import Any

from flask import Response, abort, make_response

from app.models.models import ASSET_TYPE, Asset, Manager, Site
from app.models.schemas import AssetSchema
from config import db


def read_all() -> Any:
    """This function responds to a request for /app/assets
    with the complete list of assets, sorted by asset name

    :return:    json list of all assets for all managers, all sites
    """
    assets = Asset.query.order_by(db.desc(Asset.name)).all()
    asset_schema = AssetSchema(many=True)
    data = asset_schema.dump(assets)
    return data


def read_all_for_one(manager_id: int, site_id: int) -> Any:
    """This function responds to a request for
    /app/managers/{manager_id}/sites/sites/{site_id}/assets
    with the list of all assets for one site only.

    :param manager_id:        Id of manager the site is related to
    :param site_id:           Id of the site

    :return:                  json list of all assets for 1 site
    """
    assets = (
        Asset.query.join(Manager, Manager.manager_id == Site.manager_id)
        .join(Site, Site.site_id == Asset.site_id)
        .filter(Manager.manager_id == manager_id)
        .filter(Site.site_id == site_id)
        .order_by(db.desc(Asset.name))
    )

    asset_schema = AssetSchema(many=True)
    data = asset_schema.dump(assets)
    return data


def read_one(manager_id: int, site_id: int, asset_id: int) -> Any:
    """This function responds to a request for
    /app/managers/{manager_id}/sites/{site_id}/assets/{asset_id}
    with one matching asset for the associated site and manager

    :param manager_id:        Id of manager the site is related to
    :param site_id:           Id of the site
    :param asset_id:          Id of the asset
    :return:                  json string of asset contents
    """
    asset = (
        Asset.query.join(Manager, Manager.manager_id == Site.manager_id)
        .join(Site, Site.site_id == Asset.site_id)
        .filter(Manager.manager_id == manager_id)
        .filter(Site.site_id == site_id)
        .filter(Asset.asset_id == asset_id)
        .one_or_none()
    )

    if asset is None:
        abort(404, f"Asset not found for Id: {asset_id}")

    asset_schema = AssetSchema()
    data = asset_schema.dump(asset)
    return data


def create(manager_id: int, site_id: int, asset: dict) -> tuple:
    """This function creates a new asset related to the passed in manager id, site id.

    :param manager_id:       Id of the manager that site is related to
    :param site_id:          Id of the site that asset is related to
    :param asset:            The JSON containing the asset data

    :return:                 201 on success
    """
    manager = Manager.query.filter(Manager.manager_id == manager_id).one_or_none()

    if manager is None:
        abort(404, f"Manager not found for Id: {manager_id}")

    site = (
        Site.query.filter(Manager.manager_id == manager_id)
        .filter(Site.site_id == site_id)
        .one_or_none()
    )

    if site is None:
        abort(404, f"Site not found for site Id: {site_id}.")

    schema = AssetSchema()
    new_asset = schema.load(asset, session=db.session)

    # Check the conditions for the new asset
    if new_asset.type not in ASSET_TYPE:
        abort(
            403,
            f"The asset type {new_asset.type} is not available. "
            f"Available asset types are {', '.join(ASSET_TYPE)}.",
        )

    sum_p = sum(asset.p_nominal for asset in site.assets) + new_asset.p_nominal
    if sum_p > site.p_max:
        abort(
            403,
            f"For the site {site_id}, the sum of the nominal electrical powers of the assets {sum_p} "
            f"exceeds the maximum acceptable electrical power of the site {site.p_max}.",
        )

    site.assets.append(new_asset)
    db.session.commit()
    data = schema.dump(new_asset)

    return data, 201


def update(manager_id: int, site_id: int, asset_id: int, asset: dict) -> tuple:
    """This function updates an existing asset.

    :param manager_id:       Id of the manager that site is related to
    :param site_id:          Id of the site that asset is related to
    :param asset_id:         Id of the asset to update
    :param asset:            The JSON containing the asset data to update

    :return:                 200 on success
    """
    manager = Manager.query.filter(Manager.manager_id == manager_id).one_or_none()

    if manager is None:
        abort(404, f"Manager not found for Id: {manager_id}.")

    site = (
        Site.query.filter(Manager.manager_id == manager_id)
        .filter(Site.site_id == site_id)
        .one_or_none()
    )

    if site is None:
        abort(404, f"Site not found for site Id: {site_id}.")

    update_asset = (
        Asset.query.filter(Manager.manager_id == manager_id)
        .filter(Site.site_id == site_id)
        .filter(Asset.asset_id == asset_id)
        .one_or_none()
    )

    if update_asset is None:
        abort(404, f"Asset not found for asset Id: {asset_id}.")

    schema = AssetSchema()
    update = schema.load(asset, session=db.session)

    # Check the conditions for the asset to update
    if update.type is not None and update.type not in ASSET_TYPE:
        abort(
            403,
            f"The asset type {update.type} is not available. "
            f"Available asset types are {', '.join(ASSET_TYPE)}.",
        )

    sum_p = sum(asset.p_nominal for asset in site.assets) + update_asset.p_nominal
    if update.p_nominal is not None and sum_p > site.p_max:
        abort(
            403,
            f"For the site {site_id}, the sum of the nominal electrical powers of the assets {sum_p} "
            f"exceeds the maximum acceptable electrical power of the site {site.p_max}.",
        )

    # Update the asset id
    update.site_id = update_asset.site_id
    update.asset_id = update_asset.asset_id

    db.session.merge(update)
    db.session.commit()
    data = schema.dump(update_asset)

    return data, 200


def delete(manager_id: int, site_id: int, asset_id: int) -> Response:
    """
    This function deletes an asset from the asset structure

    :param manager_id:       Id of the manager that site is related to
    :param site_id:          Id of the site that asset is related to
    :param asset_id:         Id of the asset to update
    :param asset:            The JSON containing the asset data

    :return:                 200 on successful delete, 404 if not found
    """
    asset = (
        Asset.query.filter(Manager.manager_id == manager_id)
        .filter(Site.site_id == site_id)
        .filter(Asset.asset_id == asset_id)
        .one_or_none()
    )

    if asset is None:
        abort(404, f"Asset not found for Id: {asset_id}")

    db.session.delete(asset)
    db.session.commit()
    return make_response("Asset {asset_id} deleted".format(asset_id=asset_id), 200)
