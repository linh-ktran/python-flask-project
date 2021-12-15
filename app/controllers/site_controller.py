"""This is the sites module and supports all the REST actions
for the site data"""
from typing import  List, Union

from flask import Response, abort, make_response

from app.models.models import Manager, Site
from app.models.schemas import SiteSchema, ManagerSchema
from config import db


def read_all() -> Union[dict, List[dict]]:
    """This function responds to a request for /app/sites
    with the complete list of sites, sorted by site name

    :return:                json list of all sites
    """
    sites = Site.query.order_by(db.desc(Site.name)).all()
    site_schema = SiteSchema(many=True)
    data = site_schema.dump(sites)
    return data


def create(site: dict) -> tuple:
    """This function creates a new site in responding to a request for /app/sites

    :param site:             The JSON containing the site data

    :return:                 201 on success, 404 if not found
    """
    schema = SiteSchema()

    if "managers" in site:
        managers = site.pop("managers")
        new_site = schema.load(data=site, session=db.session)
        if managers is not None:
            for manager in managers:
                associated_manager = (
                    Manager.query.filter(Manager.manager_id == manager['manager_id']).one_or_none()
                )
                if associated_manager is None:
                    abort(404, f"Manager not found for Id: {manager['manager_id']}.")

                new_site.managers.append(associated_manager)
    else:
        new_site = schema.load(data=site, session=db.session)

    db.session.add(new_site)
    db.session.commit()
    data = schema.dump(new_site)
    return data, 201


def read_one(site_id: int) -> Union[dict, List[dict]]:
    """This function responds to a request for /app/sites/{site_id}
    with one matching site for the associated manager

    :param site_id:          Id of the site

    :return:                 json string of site contents, 404 if not found
    """
    site = (Site.query.filter(Site.site_id == site_id).one_or_none())
    if site is None:
        abort(404, f"Site not found for Id: {site_id}.")

    site_schema = SiteSchema()
    data = site_schema.dump(site)
    return data


def update(site_id: int, site: dict) -> tuple:
    """This function updates an existing site related to the passed in
    manager id.

    :param site_id:          Id of the site to update
    :param content:          The JSON containing the site data

    :return:                 200 on success, 404 if not found, 403 forbidden
    """
    site_to_update = (Site.query.filter(Site.site_id == site_id).one_or_none())
    if site_to_update is None:
        abort(404, f"Site not found for Id: {site_id}.")

    schema = SiteSchema()
    update = schema.load(data=site, session=db.session)

    # Check the condition for the maximum electrical power of the site
    sum_p = sum(asset.p_nominal for asset in site_to_update.assets)
    if "p_max" in site and site["p_max"] is not None and sum_p > site['p_max']:
        abort(
            403,
            f"For the site with ID {site_id}, the sum of the nominal electrical powers of the assets {sum_p} "
            f"exceeds the new maximum electrical power of the site {site['p_max']}.",
        )

    update.site_id = site_to_update.site_id

    db.session.merge(update)
    db.session.commit()

    data = schema.dump(site_to_update)
    return data, 200


def delete(site_id: int) -> Response:
    """This function deletes a site from the site structure

    :param site_id:      Id of the site to delete

    :return:             200 on successful delete, 404 if not found
    """
    site = (
        Site.query.filter(Site.site_id == site_id).one_or_none()
    )
    if site is None:
        abort(404, f"Site not found for Id: {site_id}")

    db.session.delete(site)
    db.session.commit()
    return make_response(f"Site {site_id} deleted", 200)
