"""Manager endpoints."""

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app import db
from app.models.models import Manager, Site
from app.models.schemas import (
    ManagerCreateSchema,
    ManagerResponseSchema,
    ManagerUpdateSchema,
    MessageSchema,
)

blp = Blueprint("managers", __name__, url_prefix="/api/managers", description="Manager operations")


@blp.route("")
class ManagerList(MethodView):

    @blp.response(200, ManagerResponseSchema(many=True))
    def get(self) -> list:
        """List all managers."""
        return Manager.query.order_by(Manager.last_name).all()

    @blp.arguments(ManagerCreateSchema)
    @blp.response(201, ManagerResponseSchema)
    def post(self, data: dict) -> Manager:
        """Create a new manager. Can optionally link to existing sites via site_ids."""
        existing = Manager.query.filter_by(
            first_name=data["first_name"], last_name=data["last_name"]
        ).first()
        if existing:
            abort(409, message=f"Manager '{data['first_name']} {data['last_name']}' already exists.")

        site_ids = data.pop("site_ids", [])
        sites = []
        for site_id in site_ids:
            site = db.session.get(Site, site_id)
            if site is None:
                abort(404, message=f"Site not found for ID: {site_id}")
            sites.append(site)

        manager = Manager(first_name=data["first_name"], last_name=data["last_name"])
        manager.sites = sites

        db.session.add(manager)
        db.session.commit()
        return manager


@blp.route("/<int:manager_id>")
class ManagerDetail(MethodView):

    @blp.response(200, ManagerResponseSchema)
    def get(self, manager_id: int) -> Manager:
        """Get a single manager."""
        manager = db.session.get(Manager, manager_id)
        if manager is None:
            abort(404, message=f"Manager not found for ID: {manager_id}")
        return manager

    @blp.arguments(ManagerUpdateSchema)
    @blp.response(200, ManagerResponseSchema)
    def patch(self, data: dict, manager_id: int) -> Manager:
        """Partial update on a manager."""
        manager = db.session.get(Manager, manager_id)
        if manager is None:
            abort(404, message=f"Manager not found for ID: {manager_id}")

        if "first_name" in data:
            manager.first_name = data["first_name"]
        if "last_name" in data:
            manager.last_name = data["last_name"]
        if "site_ids" in data:
            sites = []
            for site_id in data["site_ids"]:
                site = db.session.get(Site, site_id)
                if site is None:
                    abort(404, message=f"Site not found for ID: {site_id}")
                sites.append(site)
            manager.sites = sites

        db.session.commit()
        return manager

    @blp.response(200, MessageSchema)
    def delete(self, manager_id: int) -> dict:
        """Delete a manager."""
        manager = db.session.get(Manager, manager_id)
        if manager is None:
            abort(404, message=f"Manager not found for ID: {manager_id}")

        db.session.delete(manager)
        db.session.commit()
        return {"message": f"Manager {manager_id} deleted successfully."}
