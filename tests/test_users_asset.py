import unittest

import requests

BASE_URL = "http://127.0.0.1:5000/app"
ASSETS_URL = "{}/assets".format(BASE_URL)


class AppTest(unittest.TestCase):

    site_id = 2
    NEW_ASSET = {"asset_id": 10, "name": "C5", "type": "CHILLER", "p_nominal": 2000}
    ASSET_BAD1 = {"asset_id": 6, "name": "C3", "type": "AIRCOMPRESSOR", "p_nominal": 2000}
    ASSET_BAD2 = {"asset_id": 6, "name": "C3", "type": "CHILLER", "p_nominal": 30000}
    UPDATE_ASSET = {"asset_id": 2, "name": "C3", "type": "COMPRESSOR", "p_nominal": 2500}

    def _get_add_asset_url(self, site_id: int) -> str:
        """Return the ULR for a site"""
        return "{}/site/{}/add_asset".format(BASE_URL, site_id)

    def _get_asset_url(self, site_id: int, asset_id: int) -> str:
        """Return the ULR for an asset"""
        return "{}/site/{}/asset/{}".format(BASE_URL, site_id, asset_id)

    def test_add_valid_asset(self):
        """
        POST request to /app/sites/{site_id}/add_asset to create a new asset
        """
        site_id = AppTest.site_id
        response = requests.post(
            self._get_add_asset_url(site_id=site_id), json=AppTest.NEW_ASSET
        )
        self.assertEqual(response.status_code, 201)

    def test_add_invalid_asset(self):
        """
        POST request to /app/site/{site_id}/add_asset
        with invalid asset
        """
        site_id = AppTest.site_id
        response = requests.post(
            self._get_add_asset_url(site_id=site_id), json=AppTest.ASSET_BAD1,
        )
        self.assertEqual(response.status_code, 403)
        response = requests.post(
            self._get_add_asset_url(site_id=site_id), json=AppTest.ASSET_BAD2,
        )
        self.assertEqual(response.status_code, 403)

    def test_update_invalid_asset(self):
        """
        PUT request to /app/site/{site_id}/asset/{asset_id} to update un asset
        """
        site_id = AppTest.site_id
        asset_id = AppTest.UPDATE_ASSET["asset_id"]
        response = requests.put(
            self._get_asset_url(site_id=site_id, asset_id=asset_id), json=AppTest.ASSET_BAD1,
        )
        self.assertEqual(response.status_code, 403)

        response = requests.put(
            self._get_asset_url(site_id=site_id, asset_id=asset_id), json=AppTest.ASSET_BAD2,
        )
        self.assertEqual(response.status_code, 403)

    def test_update_valid_asset(self):
        """
        PUT request to /app/site/{site_id}/asset/{asset_id} to update un asset
        """
        site_id = AppTest.site_id
        asset_id = AppTest.UPDATE_ASSET["asset_id"]
        response = requests.put(
            self._get_asset_url(site_id=site_id, asset_id=asset_id), json=AppTest.UPDATE_ASSET,
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_asset(self):
        """
        DELETE request to /app/sites/{site_id}/asset/{asset_id} to delete an asset
        """
        site_id = AppTest.site_id
        asset_id = AppTest.NEW_ASSET["asset_id"]
        requests.post(
            self._get_add_asset_url(site_id=site_id), json=AppTest.NEW_ASSET
        )
        response = requests.delete(self._get_asset_url(site_id=site_id, asset_id=asset_id))
        self.assertEqual(response.status_code, 200)

        response = requests.delete(self._get_asset_url(site_id=site_id, asset_id=asset_id))
        self.assertEqual(response.status_code, 404)
