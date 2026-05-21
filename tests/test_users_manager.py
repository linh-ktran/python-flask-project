"""Tests for the Manager API."""

import json

URL = "/api/managers"


def _post(client, data, url=URL):
    return client.post(url, data=json.dumps(data), content_type="application/json")


def _patch(client, url, data):
    return client.patch(url, data=json.dumps(data), content_type="application/json")


class TestManagerAPI:

    def test_list_empty(self, client):
        response = client.get(URL)
        assert response.status_code == 200
        assert response.json == []

    def test_list_managers(self, client, sample_manager):
        response = client.get(URL)
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]["first_name"] == "Nicolas"

    def test_get_one(self, client, sample_manager):
        response = client.get(f"{URL}/{sample_manager.id}")
        assert response.status_code == 200
        assert response.json["first_name"] == "Nicolas"
        assert "sites" in response.json

    def test_get_not_found(self, client):
        response = client.get(f"{URL}/999")
        assert response.status_code == 404

    def test_create(self, client):
        data = {"first_name": "Alice", "last_name": "Smith"}
        response = _post(client, data)
        assert response.status_code == 201
        assert response.json["first_name"] == "Alice"
        assert response.json["id"] is not None

    def test_create_with_sites(self, client, sample_site):
        data = {"first_name": "Bob", "last_name": "Jones", "site_ids": [sample_site.id]}
        response = _post(client, data)
        assert response.status_code == 201
        assert len(response.json["sites"]) == 1

    def test_create_bad_site_id(self, client):
        data = {"first_name": "Bob", "last_name": "Jones", "site_ids": [999]}
        response = _post(client, data)
        assert response.status_code == 404

    def test_create_duplicate(self, client, sample_manager):
        data = {"first_name": "Nicolas", "last_name": "Plain"}
        response = _post(client, data)
        assert response.status_code == 409

    def test_create_missing_fields(self, client):
        data = {"first_name": "Alice"}
        response = _post(client, data)
        assert response.status_code == 422

    def test_update(self, client, sample_manager):
        data = {"first_name": "Updated"}
        response = _patch(client, f"{URL}/{sample_manager.id}", data)
        assert response.status_code == 200
        assert response.json["first_name"] == "Updated"
        assert response.json["last_name"] == "Plain"  # untouched

    def test_update_not_found(self, client):
        data = {"first_name": "Ghost"}
        response = _patch(client, f"{URL}/999", data)
        assert response.status_code == 404

    def test_delete(self, client, sample_manager):
        response = client.delete(f"{URL}/{sample_manager.id}")
        assert response.status_code == 200

        # gone now
        response = client.get(f"{URL}/{sample_manager.id}")
        assert response.status_code == 404

    def test_delete_not_found(self, client):
        response = client.delete(f"{URL}/999")
        assert response.status_code == 404
