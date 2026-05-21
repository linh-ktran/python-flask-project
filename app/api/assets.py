"""Asset endpoints (nested under sites)."""

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app import db
from app.models.models import Asset, Site
from app.models.schemas import (
    AssetCreateSchema,
    AssetResponseSchema,
    AssetUpdateSchema,
    MessageSchema,
)

blp = Blueprint("assets", __name__, url_prefix="/api/sites", description="Asset operations")


@blp.route("/<int:site_id>/assets")
class AssetList(MethodView):

    @blp.response(200, AssetResponseSchema(many=True))
    def get(self, site_id: int) -> list:
        """List all assets for a given site."""
        site = db.session.get(Site, site_id)
        if site is None:
            abort(404, message=f"Site not found for ID: {site_id}")
        return site.assets

    @blp.arguments(AssetCreateSchema)
    @blp.response(201, AssetResponseSchema)
    def post(self, data: dict, site_id: int) -> Asset:
        """Add a new asset to a site. Checks power capacity before adding."""
        site = db.session.get(Site, site_id)
        if site is None:
            abort(404, message=f"Site not found for ID: {site_id}")

        new_total = site.total_power + data["nominal_power"]
        if new_total > site.max_power:
            abort(
                422,
                message=(
                    f"Cannot add asset with {data['nominal_power']}W nominal power. "
                    f"Site '{site.name}' would reach {new_total}W total, "
                    f"exceeding its maximum capacity of {site.max_power}W."
                ),
            )

        asset = Asset(
            name=data["name"],
            asset_type=data["asset_type"],
            nominal_power=data["nominal_power"],
            site_id=site_id,
        )

        db.session.add(asset)
        db.session.commit()
        return asset


@blp.route("/<int:site_id>/assets/<int:asset_id>")
class AssetDetail(MethodView):

    @blp.response(200, AssetResponseSchema)
    def get(self, site_id: int, asset_id: int) -> Asset:
        """Get a specific asset."""
        return self._get_or_404(site_id, asset_id)

    @blp.arguments(AssetUpdateSchema)
    @blp.response(200, AssetResponseSchema)
    def patch(self, data: dict, site_id: int, asset_id: int) -> Asset:
        """Update an asset. Validates power constraint if nominal_power changes."""
        asset = self._get_or_404(site_id, asset_id)
        site = asset.site

        if "nominal_power" in data:
            new_total = site.total_power - asset.nominal_power + data["nominal_power"]
            if new_total > site.max_power:
                abort(
                    422,
                    message=(
                        f"Cannot update asset power to {data['nominal_power']}W. "
                        f"Site '{site.name}' would reach {new_total}W total, "
                        f"exceeding its maximum capacity of {site.max_power}W."
                    ),
                )
            asset.nominal_power = data["nominal_power"]

        if "name" in data:
            asset.name = data["name"]
        if "asset_type" in data:
            asset.asset_type = data["asset_type"]

        db.session.commit()
        return asset

    @blp.response(200, MessageSchema)
    def delete(self, site_id: int, asset_id: int) -> dict:
        """Remove an asset from a site."""
        asset = self._get_or_404(site_id, asset_id)

        db.session.delete(asset)
        db.session.commit()
        return {"message": f"Asset '{asset.name}' (ID: {asset_id}) deleted successfully."}

    @staticmethod
    def _get_or_404(site_id: int, asset_id: int) -> Asset:
        """Look up an asset, making sure it belongs to the given site."""
        site = db.session.get(Site, site_id)
        if site is None:
            abort(404, message=f"Site not found for ID: {site_id}")

        asset = db.session.get(Asset, asset_id)
        if asset is None or asset.site_id != site_id:
            abort(404, message=f"Asset not found for ID: {asset_id} on site {site_id}")
        return asset
