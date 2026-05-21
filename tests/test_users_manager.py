"""Tests for the Manager API."""

import json


class TestManagerAPI:

    def test_list_empty(self, client):
        response = client.get("/api/managers")
        assert response.status_code == 200
        assert response.json == []

    def test_list_managers(self, client, sample_manager):
        response = client.get("/api/managers")
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]["first_name"] == "Nicolas"

    def test_get_one(self, client, sample_manager):
        response = client.get(f"/api/managers/{sample_manager.id}")
        assert response.status_code == 200
        assert response.json["first_name"] == "Nicolas"
        assert "sites" in response.json

    def test_get_not_found(self, client):
        response = client.get("/api/managers/999")
        assert response.status_code == 404

    def test_create(self, client):
        data = {"first_name": "Alice", "last_name": "Smith"}
        response = client.post("/api/managers", data=json.dumps(data), content_type="application/json")
        assert response.status_code == 201
        assert response.json["first_name"] == "Alice"
        assert response.json["id"] is not None

    def test_create_with_sites(self, client, sample_site):
        data = {"first_name": "Bob", "last_name": "Jones", "site_ids": [sample_site.id]}
        response = client.post("/api/managers", data=json.dumps(data), content_type="application/json")
        assert response.status_code == 201
        assert len(response.json["sites"]) == 1

    def test_create_bad_site_id(self, client):
        data = {"first_name": "Bob", "last_name": "Jones", "site_ids": [999]}
        response = client.post("/api/managers", data=json.dumps(data), content_type="application/json")
        assert response.status_code == 404

    def test_create_duplicate(self, client, sample_manager):
        data = {"first_name": "Nicolas", "last_name": "Plain"}
        response = client.post("/api/managers", data=json.dumps(data), content_type="application/json")
        assert response.status_code == 409

    def test_create_missing_fields(self, client):
        data = {"first_name": "Alice"}
        response = client.post("/api/managers", data=json.dumps(data), content_type="application/json")
        assert response.status_code == 422

    def test_update(self, client, sample_manager):
        data = {"first_name": "Updated"}
        response = client.patch(
            f"/api/managers/{sample_manager.id}", data=json.dumps(data), content_type="application/json"
        )
        assert response.status_code == 200
        assert response.json["first_name"] == "Updated"
        assert response.json["last_name"] == "Plain"  # untouched

    def test_update_not_found(self, client):
        data = {"first_name": "Ghost"}
        response = client.patch("/api/managers/999", data=json.dumps(data), content_type="application/json")
        assert response.status_code == 404

    def test_delete(self, client, sample_manager):
        response = client.delete(f"/api/managers/{sample_manager.id}")
        assert response.status_code == 200

        # gone now
        response = client.get(f"/api/managers/{sample_manager.id}")
        assert response.status_code == 404

    def test_delete_not_found(self, client):
        response = client.delete("/api/managers/999")
        assert response.status_code == 404
