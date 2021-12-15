"""This is the manager module and supports all the ReST actions for the manager data"""
from typing import  List, Union

from flask import Response, abort, make_response

from app.models.models import Manager, Site
from app.models.schemas import ManagerSchema
from config import db


def read_all() -> Union[dict, List[dict]]:
    """This function responds to a request for /api/managers
    with the lists of all managers

    :return:        json string of list of managers
    """
    manager = Manager.query.order_by(Manager.lname).all()
    manager_schema = ManagerSchema(many=True)
    data = manager_schema.dump(manager)
    return data


def read_one(manager_id: int) -> Union[dict, List[dict]]:
    """This function responds to a request for /api/managers/{manager_id}
    with one matching manager from managers

    :param manager_id:   Id of manager to find

    :return:             manager matching id, 404 on manager not found
    """
    manager = Manager.query.filter(Manager.manager_id == manager_id).one_or_none()#.outerjoin(Site)

    if manager is None:
        abort(404, f"Manager not found for Id: {manager_id}")

    manager_schema = ManagerSchema()
    data = manager_schema.dump(manager)
    return data


def create(manager: dict) -> tuple:
    """This function creates a new manager in the manager structure
    based on the passed in manager data

    :param manager:  manager to create in manager structure

    :return:         201 on success, 409 on manager exists, 404 if not found
    """
    fname = manager.get("fname")
    lname = manager.get("lname")

    existing_manager = (
        Manager.query.filter(Manager.fname == fname).filter(Manager.lname == lname).one_or_none()
    )
    if existing_manager is not None:
        abort(409, f"Manager {fname} {lname} exists already")

    schema = ManagerSchema()
    if "sites" in manager:
        sites = manager.pop("sites")
        new_manager = schema.load(data=manager, session=db.session)

        if sites is not None:
            for site in sites:
                associated_site = (
                    Site.query.filter(Site.site_id == site['site_id']).one_or_none()
                )
                if associated_site is None:
                    abort(404, f"Site not found for Id: {site['site_id']}")

                new_manager.sites.append(associated_site)
    else:
        new_manager = schema.load(data=manager, session=db.session)

    db.session.add(new_manager)
    db.session.commit()

    data = schema.dump(new_manager)
    return data, 201


def update(manager_id: int, manager: dict) -> tuple:
    """This function updates an existing manager in the manager structure
    Raise an error if a manager with the name we want to update to
    already exists in the database.

    :param manager_id:   Id of the manager to update in the manager structure
    :param manager:      manager to update

    :return:             updated manager structure, 404 on manager not found, 403 forbidden
    """
    manager_to_update = Manager.query.filter(Manager.manager_id == manager_id).one_or_none()
    if manager_to_update is None:
        abort(404, f"Manager not found for Id: {manager_id}")

    schema = ManagerSchema()
    update = schema.load(data=manager, session=db.session)

    update.manager_id = manager_to_update.manager_id

    db.session.merge(update)
    db.session.commit()

    data = schema.dump(manager_to_update)
    return data, 200


def delete(manager_id: int) -> Response:
    """This function deletes a manager from the manager structure

    :param manager_id:   Id of the manager to delete

    :return:             200 on successful delete, 404 on manager not found
    """
    # Get the manager requested
    manager = Manager.query.filter(Manager.manager_id == manager_id).one_or_none()

    if manager is None:
        abort(404, f"Manager not found for Id: {manager_id}")

    db.session.delete(manager)
    db.session.commit()
    return make_response(f"Manager {manager_id} deleted", 200)
