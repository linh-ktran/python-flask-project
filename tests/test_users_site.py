"""Tests for the Site API."""

import json

URL = "/api/sites"


def _post(client, data, url=URL):
    return client.post(url, data=json.dumps(data), content_type="application/json")


def _patch(client, url, data):
    return client.patch(url, data=json.dumps(data), content_type="application/json")


class TestSiteAPI:

    def test_list_empty(self, client):
        response = client.get(URL)
        assert response.status_code == 200
        assert response.json == []

    def test_list_sites(self, client, sample_site):
        response = client.get(URL)
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]["name"] == "Orsay"

    def test_get_with_assets(self, client, sample_site_with_assets):
        response = client.get(f"{URL}/{sample_site_with_assets.id}")
        assert response.status_code == 200
        assert response.json["name"] == "Tarnos"
        assert response.json["max_power"] == 10000
        assert response.json["total_power"] == 5000
        assert response.json["available_power"] == 5000
        assert len(response.json["assets"]) == 2

    def test_get_not_found(self, client):
        response = client.get(f"{URL}/999")
        assert response.status_code == 404

    def test_create(self, client):
        data = {"name": "NewSite", "address": "123 Street", "max_power": 15000}
        response = _post(client, data)
        assert response.status_code == 201
        assert response.json["name"] == "NewSite"
        assert response.json["assets"] == []

    def test_create_with_managers(self, client, sample_manager):
        data = {
            "name": "Linked", "address": "456 St",
            "max_power": 10000, "manager_ids": [sample_manager.id],
        }
        response = _post(client, data)
        assert response.status_code == 201
        assert len(response.json["managers"]) == 1

    def test_create_bad_manager_id(self, client):
        data = {"name": "Bad", "address": "789 St", "max_power": 5000, "manager_ids": [999]}
        response = _post(client, data)
        assert response.status_code == 404

    def test_create_missing_fields(self, client):
        data = {"name": "Incomplete"}
        response = _post(client, data)
        assert response.status_code == 422

    def test_update(self, client, sample_site):
        data = {"name": "Updated Site", "address": "New Address"}
        response = _patch(client, f"{URL}/{sample_site.id}", data)
        assert response.status_code == 200
        assert response.json["name"] == "Updated Site"
        assert response.json["max_power"] == 18000  # unchanged

    def test_update_max_power_too_low(self, client, sample_site_with_assets):
        # total power is 5000, so setting max to 1000 should fail
        data = {"max_power": 1000}
        response = _patch(client, f"{URL}/{sample_site_with_assets.id}", data)
        assert response.status_code == 422

    def test_update_not_found(self, client):
        data = {"name": "Ghost"}
        response = _patch(client, f"{URL}/999", data)
        assert response.status_code == 404

    def test_delete(self, client, sample_site):
        response = client.delete(f"{URL}/{sample_site.id}")
        assert response.status_code == 200

        response = client.get(f"{URL}/{sample_site.id}")
        assert response.status_code == 404

    def test_delete_cascades_assets(self, client, sample_site_with_assets):
        site_id = sample_site_with_assets.id
        response = client.delete(f"{URL}/{site_id}")
        assert response.status_code == 200

        # assets should be gone too
        response = client.get(f"{URL}/{site_id}/assets")
        assert response.status_code == 404

    def test_delete_not_found(self, client):
        response = client.delete(f"{URL}/999")
        assert response.status_code == 404
