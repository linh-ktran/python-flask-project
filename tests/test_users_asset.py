"""Tests for the Asset API."""

import json


class TestAssetAPI:

    def test_list_assets(self, client, sample_site_with_assets):
        response = client.get(f"/api/sites/{sample_site_with_assets.id}/assets")
        assert response.status_code == 200
        assert len(response.json) == 2

    def test_list_assets_site_not_found(self, client):
        response = client.get("/api/sites/999/assets")
        assert response.status_code == 404

    def test_create(self, client, sample_site):
        data = {"name": "NewChiller", "asset_type": "CHILLER", "nominal_power": 5000}
        response = client.post(
            f"/api/sites/{sample_site.id}/assets", data=json.dumps(data), content_type="application/json"
        )
        assert response.status_code == 201
        assert response.json["name"] == "NewChiller"
        assert response.json["asset_type"] == "CHILLER"
        assert response.json["site_id"] == sample_site.id

    def test_create_exceeds_power(self, client, sample_site_with_assets):
        # max=10000, current=5000, so adding 6000 should fail
        data = {"name": "BigMachine", "asset_type": "FURNACE", "nominal_power": 6000}
        response = client.post(
            f"/api/sites/{sample_site_with_assets.id}/assets",
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 422

    def test_create_bad_type(self, client, sample_site):
        data = {"name": "Bad", "asset_type": "INVALID_TYPE", "nominal_power": 1000}
        response = client.post(
            f"/api/sites/{sample_site.id}/assets", data=json.dumps(data), content_type="application/json"
        )
        assert response.status_code == 422

    def test_create_site_not_found(self, client):
        data = {"name": "Orphan", "asset_type": "CHILLER", "nominal_power": 1000}
        response = client.post("/api/sites/999/assets", data=json.dumps(data), content_type="application/json")
        assert response.status_code == 404

    def test_create_missing_fields(self, client, sample_site):
        data = {"name": "Incomplete"}
        response = client.post(
            f"/api/sites/{sample_site.id}/assets", data=json.dumps(data), content_type="application/json"
        )
        assert response.status_code == 422

    def test_get_one(self, client, sample_site_with_assets):
        asset = sample_site_with_assets.assets[0]
        response = client.get(f"/api/sites/{sample_site_with_assets.id}/assets/{asset.id}")
        assert response.status_code == 200
        assert response.json["name"] == asset.name

    def test_get_not_found(self, client, sample_site):
        response = client.get(f"/api/sites/{sample_site.id}/assets/999")
        assert response.status_code == 404

    def test_update(self, client, sample_site_with_assets):
        asset = sample_site_with_assets.assets[0]
        data = {"name": "Renamed", "nominal_power": 4000}
        response = client.patch(
            f"/api/sites/{sample_site_with_assets.id}/assets/{asset.id}",
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 200
        assert response.json["name"] == "Renamed"
        assert response.json["nominal_power"] == 4000

    def test_update_exceeds_power(self, client, sample_site_with_assets):
        asset = sample_site_with_assets.assets[0]
        # max=10000, other=2000, setting this to 9000 => 11000 > 10000
        data = {"nominal_power": 9000}
        response = client.patch(
            f"/api/sites/{sample_site_with_assets.id}/assets/{asset.id}",
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 422

    def test_update_bad_type(self, client, sample_site_with_assets):
        asset = sample_site_with_assets.assets[0]
        data = {"asset_type": "NOT_A_TYPE"}
        response = client.patch(
            f"/api/sites/{sample_site_with_assets.id}/assets/{asset.id}",
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 422

    def test_delete(self, client, sample_site_with_assets):
        asset = sample_site_with_assets.assets[0]
        response = client.delete(f"/api/sites/{sample_site_with_assets.id}/assets/{asset.id}")
        assert response.status_code == 200

        # gone
        response = client.get(f"/api/sites/{sample_site_with_assets.id}/assets/{asset.id}")
        assert response.status_code == 404

    def test_delete_not_found(self, client, sample_site):
        response = client.delete(f"/api/sites/{sample_site.id}/assets/999")
        assert response.status_code == 404
