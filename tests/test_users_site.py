"""Tests for the Site API."""

import json


class TestSiteAPI:

    def test_list_empty(self, client):
        response = client.get("/api/sites")
        assert response.status_code == 200
        assert response.json == []

    def test_list_sites(self, client, sample_site):
        response = client.get("/api/sites")
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]["name"] == "Orsay"

    def test_get_with_assets(self, client, sample_site_with_assets):
        response = client.get(f"/api/sites/{sample_site_with_assets.id}")
        assert response.status_code == 200
        assert response.json["name"] == "Tarnos"
        assert response.json["max_power"] == 10000
        assert response.json["total_power"] == 5000
        assert response.json["available_power"] == 5000
        assert len(response.json["assets"]) == 2

    def test_get_not_found(self, client):
        response = client.get("/api/sites/999")
        assert response.status_code == 404

    def test_create(self, client):
        data = {"name": "NewSite", "address": "123 Street", "max_power": 15000}
        response = client.post("/api/sites", data=json.dumps(data), content_type="application/json")
        assert response.status_code == 201
        assert response.json["name"] == "NewSite"
        assert response.json["assets"] == []

    def test_create_with_managers(self, client, sample_manager):
        data = {"name": "Linked", "address": "456 St", "max_power": 10000, "manager_ids": [sample_manager.id]}
        response = client.post("/api/sites", data=json.dumps(data), content_type="application/json")
        assert response.status_code == 201
        assert len(response.json["managers"]) == 1

    def test_create_bad_manager_id(self, client):
        data = {"name": "Bad", "address": "789 St", "max_power": 5000, "manager_ids": [999]}
        response = client.post("/api/sites", data=json.dumps(data), content_type="application/json")
        assert response.status_code == 404

    def test_create_missing_fields(self, client):
        data = {"name": "Incomplete"}
        response = client.post("/api/sites", data=json.dumps(data), content_type="application/json")
        assert response.status_code == 422

    def test_update(self, client, sample_site):
        data = {"name": "Updated Site", "address": "New Address"}
        response = client.patch(
            f"/api/sites/{sample_site.id}", data=json.dumps(data), content_type="application/json"
        )
        assert response.status_code == 200
        assert response.json["name"] == "Updated Site"
        assert response.json["max_power"] == 18000  # unchanged

    def test_update_max_power_too_low(self, client, sample_site_with_assets):
        # total power is 5000, so setting max to 1000 should fail
        data = {"max_power": 1000}
        response = client.patch(
            f"/api/sites/{sample_site_with_assets.id}", data=json.dumps(data), content_type="application/json"
        )
        assert response.status_code == 422

    def test_update_not_found(self, client):
        data = {"name": "Ghost"}
        response = client.patch("/api/sites/999", data=json.dumps(data), content_type="application/json")
        assert response.status_code == 404

    def test_delete(self, client, sample_site):
        response = client.delete(f"/api/sites/{sample_site.id}")
        assert response.status_code == 200

        response = client.get(f"/api/sites/{sample_site.id}")
        assert response.status_code == 404

    def test_delete_cascades_assets(self, client, sample_site_with_assets):
        site_id = sample_site_with_assets.id
        response = client.delete(f"/api/sites/{site_id}")
        assert response.status_code == 200

        # assets should be gone too
        response = client.get(f"/api/sites/{site_id}/assets")
        assert response.status_code == 404

    def test_delete_not_found(self, client):
        response = client.delete("/api/sites/999")
        assert response.status_code == 404
