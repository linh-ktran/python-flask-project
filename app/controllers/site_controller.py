"""This is the sites module and supports all the REST actions
for the site data"""
from typing import  List, Union

from flask import Response, abort, make_response

from app.models.models import Manager, Site
from app.models.schemas import SiteSchema
from config import db


def read_all() -> Union[dict, List[dict]]:
    """This function responds to a request for /app/sites
    with the complete list of sites, sorted by site name

    :return:                json list of all sites for all managers
    """
    sites = Site.query.order_by(db.desc(Site.name)).all()
    site_schema = SiteSchema(many=True)
    data = site_schema.dump(sites)
    return data


def read_all_for_one(manager_id: int) -> Union[dict, List[dict]]:
    """This function responds to a request for /app/managers/{manager_id}/sites
    with the list of sites associated with a manager only.

    :param manager_id:      Id of manager the site is related to

    :return:                json list of all sites for 1 manager
    """
    sites = (
        Site.query.join(Manager, Manager.manager_id == Site.manager_id)
        .filter(Manager.manager_id == manager_id)
        .order_by(db.desc(Site.name))
    )

    site_schema = SiteSchema(many=True)
    data = site_schema.dump(sites)
    return data


def read_one(manager_id: int, site_id: int) -> Union[dict, List[dict]]:
    """This function responds to a request for
    /app/managers/{manager_id}/sites/{site_id}
    with one matching site for the associated manager

    :param manager_id:       Id of manager the site is related to
    :param site_id:          Id of the site

    :return:                 json string of site contents
    """
    site = (
        Site.query.join(Manager, Manager.manager_id == Site.manager_id)
        .filter(Manager.manager_id == manager_id)
        .filter(Site.site_id == site_id)
        .one_or_none()
    )
    if site is None:
        abort(404, f"Site not found for Id: {site_id}")

    site_schema = SiteSchema()
    data = site_schema.dump(site)
    return data


def create(manager_id: int, site: dict) -> tuple:
    """This function creates a new site related a manager.

    :param manager_id:       Id of the manager the site is related to
    :param site:             The JSON containing the site data

    :return:                 201 on success
    """
    manager = Manager.query.filter(Manager.manager_id == manager_id).one_or_none()
    if manager is None:
        abort(404, f"Manager not found for Id: {manager_id}")

    schema = SiteSchema()
    new_site = schema.load(site, session=db.session)

    manager.sites.append(new_site)
    db.session.commit()

    data = schema.dump(new_site)
    return data, 201


def update(manager_id: int, site_id: int, site: dict) -> tuple:
    """This function updates an existing site related to the passed in
    manager id.

    :param manager_id:       Id of the manager the site is related to
    :param site_id:          Id of the site to update
    :param content:          The JSON containing the site data

    :return:                 200 on success
    """
    update_site = (
        Site.query.filter(Manager.manager_id == manager_id)
        .filter(Site.site_id == site_id)
        .one_or_none()
    )

    if update_site is None:
        abort(404, f"Site not found for Id: {site_id}")

    schema = SiteSchema()
    update = schema.load(site, session=db.session)
    update.manager_id = update_site.manager_id
    update.site_id = update_site.site_id

    db.session.merge(update)
    db.session.commit()
    data = schema.dump(update_site)

    return data, 200


def delete(manager_id: int, site_id: int) -> Response:
    """This function deletes a site from the site structure

    :param manager_id:   Id of the manager the site is related to
    :param site_id:      Id of the site to delete
    :return:             200 on successful delete, 404 if not found
    """
    site = (
        Site.query.filter(Manager.manager_id == manager_id)
        .filter(Site.site_id == site_id)
        .one_or_none()
    )
    if site is None:
        abort(404, f"Site not found for Id: {site_id}")

    db.session.delete(site)
    db.session.commit()
    return make_response(f"Site {site_id} deleted", 200)
