import unittest

import requests

BASE_URL = "http://127.0.0.1:5000/app"
ASSETS_URL = "{}/assets".format(BASE_URL)


class AppTest(unittest.TestCase):

    ASSET_OBJ = {"asset_id": 3, "name": "C3", "type": "CHILLER", "p_nominal": 2000}
    ASSET_OBJ_BAD1 = {"asset_id": 3, "name": "C3", "type": "CHILLERR", "p_nominal": 2000}
    ASSET_OBJ_BAD2 = {"asset_id": 3, "name": "C3", "type": "CHILLER", "p_nominal": 20000}

    ASSET_OBJ_TEST = {
        "asset_id": 3,
        "name": "C3",
        "type": "CHILLER",
        "p_nominal": 2000,
        "site": {"site_id": 1},
    }

    UPDATE_ASSET_OBJ = {
        "asset_id": 3,
        "type": "COMPRESSOR",
        "p_nominal": 2500,
    }

    UPDATE_ASSET_OBJ_TEST = {
        "asset_id": 3,
        "name": "C3",
        "type": "COMPRESSOR",
        "p_nominal": 2500,
        "site": {"site_id": 1},
    }

    def _get_assets_url(self, manager_id: int, site_id: int) -> str:
        """Return the ULR for list of assets"""
        return "{}/managers/{}/sites/{}/assets".format(BASE_URL, manager_id, site_id)

    def _get_asset_url(self, manager_id: int, site_id: int, asset_id: int) -> str:
        """Return the ULR for an asset"""
        return "{}/managers/{}/sites/{}/assets/{}".format(BASE_URL, manager_id, site_id, asset_id)

    def test_1_get_assets(self):
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

    def test_2_add_new_asset(self):
        """
        POST request to /app/managers/{manager_id}/sites/{site_id}/assets
        to create a new asset and check if the new asset is actually added
        """
        manager_id, site_id = 1, 1
        asset_id = AppTest.ASSET_OBJ["asset_id"]
        # Bad asset
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

        # Good asset
        response = requests.post(
            self._get_assets_url(manager_id=manager_id, site_id=site_id), json=AppTest.ASSET_OBJ
        )
        self.assertEqual(response.status_code, 201)
        response = requests.get(
            self._get_asset_url(manager_id=manager_id, site_id=site_id, asset_id=asset_id)
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), AppTest.ASSET_OBJ_TEST)

    def test_3_update_existing_asset(self):
        """
        PUT request to /app/managers/{manager_id}/sites/{site_id}/assets/{asset_id}
        GET request to /app/managers/{manager_id}/sites/{site_id}/assets/{asset_id}
        to update un asset and check if the new asset is actually updated
        """
        manager_id, site_id = 1, 1

        asset_id = AppTest.ASSET_OBJ["asset_id"]
        response = requests.put(
            self._get_asset_url(manager_id=manager_id, site_id=site_id, asset_id=asset_id),
            json=AppTest.UPDATE_ASSET_OBJ,
        )
        self.assertEqual(response.status_code, 200)
        response = requests.get(
            self._get_asset_url(manager_id=manager_id, site_id=site_id, asset_id=asset_id)
        )

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), AppTest.UPDATE_ASSET_OBJ_TEST)

        # Update with bad info
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

    def test_4_delete_asset(self):
        """
        DELETE request to /app/managers/{manager_id}/sites/{site_id}/assets/{asset_id}
        to delete an asset and check if the asset is actually deleted
        """
        manager_id, site_id = 1, 1
        asset_id = AppTest.UPDATE_ASSET_OBJ["asset_id"]
        bad_asset_id = 10
        response = requests.delete(
            self._get_asset_url(manager_id=manager_id, site_id=site_id, asset_id=asset_id)
        )
        self.assertEqual(response.status_code, 200)
        response = requests.get(
            self._get_asset_url(manager_id=manager_id, site_id=site_id, asset_id=asset_id)
        )
        self.assertEqual(response.status_code, 404)
        response = requests.delete(
            self._get_asset_url(manager_id=manager_id, site_id=site_id, asset_id=bad_asset_id)
        )
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
