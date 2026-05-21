"""Site endpoints."""

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app import db
from app.models.models import Manager, Site
from app.models.schemas import (
    MessageSchema,
    SiteCreateSchema,
    SiteResponseSchema,
    SiteUpdateSchema,
)

blp = Blueprint("sites", __name__, url_prefix="/api/sites", description="Site operations")


@blp.route("")
class SiteList(MethodView):

    @blp.response(200, SiteResponseSchema(many=True))
    def get(self) -> list:
        """List all sites."""
        return Site.query.order_by(Site.name).all()

    @blp.arguments(SiteCreateSchema)
    @blp.response(201, SiteResponseSchema)
    def post(self, data: dict) -> Site:
        """Create a new site. Can optionally link to managers via manager_ids."""
        manager_ids = data.pop("manager_ids", [])
        managers = []
        for manager_id in manager_ids:
            manager = db.session.get(Manager, manager_id)
            if manager is None:
                abort(404, message=f"Manager not found for ID: {manager_id}")
            managers.append(manager)

        site = Site(name=data["name"], address=data["address"], max_power=data["max_power"])
        site.managers = managers

        db.session.add(site)
        db.session.commit()
        return site


@blp.route("/<int:site_id>")
class SiteDetail(MethodView):

    @blp.response(200, SiteResponseSchema)
    def get(self, site_id: int) -> Site:
        """Get a site with its assets and power usage info."""
        site = db.session.get(Site, site_id)
        if site is None:
            abort(404, message=f"Site not found for ID: {site_id}")
        return site

    @blp.arguments(SiteUpdateSchema)
    @blp.response(200, SiteResponseSchema)
    def patch(self, data: dict, site_id: int) -> Site:
        """Partial update. Will reject max_power below current usage."""
        site = db.session.get(Site, site_id)
        if site is None:
            abort(404, message=f"Site not found for ID: {site_id}")

        if "max_power" in data:
            new_max = data["max_power"]
            if site.total_power > new_max:
                abort(
                    422,
                    message=(
                        f"Cannot set max_power to {new_max}W. "
                        f"Current total asset power is {site.total_power}W, "
                        f"which exceeds the new limit."
                    ),
                )
            site.max_power = new_max

        if "name" in data:
            site.name = data["name"]
        if "address" in data:
            site.address = data["address"]
        if "manager_ids" in data:
            managers = []
            for manager_id in data["manager_ids"]:
                manager = db.session.get(Manager, manager_id)
                if manager is None:
                    abort(404, message=f"Manager not found for ID: {manager_id}")
                managers.append(manager)
            site.managers = managers

        db.session.commit()
        return site

    @blp.response(200, MessageSchema)
    def delete(self, site_id: int) -> dict:
        """Delete a site (cascades to its assets)."""
        site = db.session.get(Site, site_id)
        if site is None:
            abort(404, message=f"Site not found for ID: {site_id}")

        db.session.delete(site)
        db.session.commit()
        return {"message": f"Site '{site.name}' (ID: {site_id}) deleted successfully."}
