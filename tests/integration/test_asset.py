import unittest

import requests

BASE_URL = "http://127.0.0.1:5000/app"
ASSETS_URL = "{}/assets".format(BASE_URL)


class AppTest(unittest.TestCase):
    manager_id, site_id = 1, 1
    ASSET_OBJ_BAD1 = {"asset_id": 6, "name": "C3", "type": "AIRCOMPRESSOR", "p_nominal": 2000}
    ASSET_OBJ_BAD2 = {"asset_id": 6, "name": "C3", "type": "CHILLER", "p_nominal": 50000}

    ASSET_OBJ = {"asset_id": 6, "name": "C3", "type": "CHILLER", "p_nominal": 2000}
    ASSET_OBJ_CHECK= {
        "asset_id": 6,
        "name": "C3",
        "type": "CHILLER",
        "p_nominal": 2000,
        "site": {"site_id": site_id},
    }

    UPDATE_ASSET_OBJ = {"asset_id": 2, "name": "C3", "type": "COMPRESSOR", "p_nominal": 2500}
    UPDATE_ASSET_OBJ_CHECK = {
        "asset_id": 2,
        "name": "C3",
        "type": "COMPRESSOR",
        "p_nominal": 2500,
        "site": {"site_id": site_id},
    }

    ASSET_OBJ_DELETE = {"asset_id": 10, "name": "C7", "type": "COMPRESSOR", "p_nominal": 2000}

    def _get_assets_url(self, manager_id: int, site_id: int) -> str:
        """Return the ULR for list of assets"""
        return "{}/managers/{}/sites/{}/assets".format(BASE_URL, manager_id, site_id)

    def _get_asset_url(self, manager_id: int, site_id: int, asset_id: int) -> str:
        """Return the ULR for an asset"""
        return "{}/managers/{}/sites/{}/assets/{}".format(BASE_URL, manager_id, site_id, asset_id)

    def test_get_assets(self):
        """
        GET request to /app/assets returns the details of all assets
        and to /app/managers/{manager_id}/sites returns the assets for 1 site
        and to /app/managers/{manager_id}/sites/{site_id}/assets/{asset_id} returns one specific asset
        """
        manager_id, site_id, asset_id = 1, 1, 1
        response = requests.get(ASSETS_URL)
        self.assertEqual(response.status_code, 200)
        response = requests.get(self._get_assets_url(manager_id=manager_id, site_id=site_id))
        self.assertEqual(response.status_code, 200)
        response = requests.get(
            self._get_asset_url(manager_id=manager_id, site_id=site_id, asset_id=asset_id)
        )
        self.assertEqual(response.status_code, 200)

    def test_add_valid_asset(self):
        """
        POST request to /app/managers/{manager_id}/sites/{site_id}/assets
        to create a new asset and check if the new asset is actually added
        """
        manager_id = AppTest.manager_id
        site_id = AppTest.site_id
        response = requests.post(
            self._get_assets_url(manager_id=manager_id, site_id=site_id), json=AppTest.ASSET_OBJ
        )
        self.assertEqual(response.status_code, 201)

        asset_id = AppTest.ASSET_OBJ["asset_id"]
        response = requests.get(
            self._get_asset_url(manager_id=manager_id, site_id=site_id, asset_id=asset_id)
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), AppTest.ASSET_OBJ_CHECK)

    def test_add_invalid_asset(self):
        """
        POST request to /app/managers/{manager_id}/sites/{site_id}/assets
        with invalid asset
        """
        manager_id = AppTest.manager_id
        site_id = AppTest.site_id
        response = requests.post(
            self._get_assets_url(manager_id=manager_id, site_id=site_id),
            json=AppTest.ASSET_OBJ_BAD1,
        )
        self.assertEqual(response.status_code, 403)
        response = requests.post(
            self._get_assets_url(manager_id=manager_id, site_id=site_id),
            json=AppTest.ASSET_OBJ_BAD2,
        )
        self.assertEqual(response.status_code, 403)

    def test_update_invalid_asset(self):
        """
        PUT request to /app/managers/{manager_id}/sites/{site_id}/assets/{asset_id}
        GET request to /app/managers/{manager_id}/sites/{site_id}/assets/{asset_id}
        to update un asset and check if the new asset is actually updated
        """
        manager_id = AppTest.manager_id
        site_id = AppTest.site_id
        asset_id = AppTest.UPDATE_ASSET_OBJ["asset_id"]
        response = requests.put(
            self._get_asset_url(manager_id=manager_id, site_id=site_id, asset_id=asset_id),
            json=AppTest.ASSET_OBJ_BAD1,
        )
        self.assertEqual(response.status_code, 403)

        response = requests.put(
            self._get_asset_url(manager_id=manager_id, site_id=site_id, asset_id=asset_id),
            json=AppTest.ASSET_OBJ_BAD2,
        )
        self.assertEqual(response.status_code, 403)

    def test_update_valid_asset(self):
        """
        PUT request to /app/managers/{manager_id}/sites/{site_id}/assets/{asset_id}
        GET request to /app/managers/{manager_id}/sites/{site_id}/assets/{asset_id}
        to update un asset and check if the new asset is actually updated
        """
        manager_id = AppTest.manager_id
        site_id = AppTest.site_id
        asset_id = AppTest.UPDATE_ASSET_OBJ["asset_id"]
        response = requests.put(
            self._get_asset_url(manager_id=manager_id, site_id=site_id, asset_id=asset_id),
            json=AppTest.UPDATE_ASSET_OBJ,
        )
        self.assertEqual(response.status_code, 200)

        response = requests.get(
            self._get_asset_url(manager_id=manager_id, site_id=site_id, asset_id=asset_id)
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), AppTest.UPDATE_ASSET_OBJ_CHECK)

    def test_delete_asset(self):
        """
        DELETE request to /app/managers/{manager_id}/sites/{site_id}/assets/{asset_id}
        to delete an asset and check if the asset is actually deleted
        """
        manager_id = AppTest.manager_id
        site_id = AppTest.site_id
        asset_id = AppTest.ASSET_OBJ_DELETE["asset_id"]
        response = requests.post(
            self._get_assets_url(manager_id=manager_id, site_id=site_id), json=AppTest.ASSET_OBJ_DELETE
        )
        self.assertEqual(response.status_code, 201)
        response = requests.delete(
            self._get_asset_url(manager_id=manager_id, site_id=site_id, asset_id=asset_id)
        )
        self.assertEqual(response.status_code, 200)
        response = requests.get(
            self._get_asset_url(manager_id=manager_id, site_id=site_id, asset_id=asset_id)
        )
        self.assertEqual(response.status_code, 404)
        response = requests.delete(
            self._get_asset_url(manager_id=manager_id, site_id=site_id, asset_id=asset_id)
        )
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
