"""This is the asset module and supports all the REST actions for the asset data"""
from typing import  List, Union

from flask import Response, abort, make_response

from app.models.models import ASSET_TYPE, Asset, Manager, Site
from app.models.schemas import AssetSchema
from config import db


def create(site_id: int, asset: dict) -> tuple:
    """This function creates a new asset related to the passed in site id.

    :param manager_id:       Id of the manager that site is related to
    :param site_id:          Id of the site that asset is related to
    :param asset:            The JSON containing the asset data

    :return:                 201 on success, 404 if not found, 403 forbidden
    """
    site = (Site.query.filter(Site.site_id == site_id).one_or_none())
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


def update(site_id: int, asset_id: int, asset: dict) -> tuple:
    """This function updates an existing asset.

    :param site_id:          Id of the site that asset is related to
    :param asset_id:         Id of the asset to update
    :param asset:            The JSON containing the asset data to update

    :return:                 200 on success, 404 if not found, 403 forbidden
    """
    site = (Site.query.filter(Site.site_id == site_id).one_or_none())

    if site is None:
        abort(404, f"Site not found for site Id: {site_id}.")

    asset_to_update = (
        Asset.query.filter(Site.site_id == site_id).filter(Asset.asset_id == asset_id)
            .one_or_none()
    )

    if asset_to_update is None:
        abort(404, f"Asset not found for asset Id: {asset_id}.")

    schema = AssetSchema()
    update = schema.load(asset, session=db.session)

    # Check the condition for the asset type to update
    if update.type is not None and update.type not in ASSET_TYPE:
        abort(
            403,
            f"The asset type {update.type} is not available. "
            f"Available asset types are {', '.join(ASSET_TYPE)}.",
        )

    # Check the condition for the maximum electrical power of the site
    if update.p_nominal is not None:
        sum_p = sum(asset.p_nominal for asset in site.assets) + update.p_nominal - asset_to_update.p_nominal
        if sum_p > site.p_max:
            abort(
                403,
                f"For the site with ID {site_id}, the sum of the nominal electrical powers "
                f"of the assets {sum_p} exceeds the maximum acceptable electrical power "
                f"of the site {site.p_max}.",
            )

    # Update the asset id
    update.site_id = asset_to_update.site_id
    update.asset_id = asset_to_update.asset_id

    db.session.merge(update)
    db.session.commit()
    data = schema.dump(asset_to_update)

    return data, 200


def delete(site_id: int, asset_id: int) -> Response:
    """
    This function deletes an asset from the asset structure

    :param site_id:          Id of the site that asset is related to
    :param asset_id:         Id of the asset to update
    :param asset:            The JSON containing the asset data

    :return:                 200 on successful delete, 404 if not found
    """
    asset = (
        Asset.query
        .filter(Site.site_id == site_id)
        .filter(Asset.asset_id == asset_id)
        .one_or_none()
    )

    if asset is None:
        abort(404, f"Asset not found for Id: {asset_id}")

    db.session.delete(asset)
    db.session.commit()
    return make_response("Asset {asset_id} deleted".format(asset_id=asset_id), 200)
