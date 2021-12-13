import unittest
import requests


class AppTest(unittest.TestCase):
    API_URL = "http://127.0.0.1:5000/app"
    ASSETS_URL = "{}/assets".format(API_URL)

    ASSET_OBJ = {"asset_id": 4, "name": "C5", "type": "CHILLER", "p_nominal": 2000}

    ASSET_OBJ_TEST = {
        "asset_id": 4,
        "name": "C5",
        "type": "CHILLER",
        "p_nominal": 2000,
        "site": {"address": "20 rue de Paris", "name": "Orsay", "p_max": 18000, "site_id": 1},
    }

    UPDATE_ASSET_OBJ = {
        "asset_id": 4,
        "type": "COMPRESSOR",
        "p_nominal": 2500,
    }

    UPDATE_ASSET_OBJ_TEST = {
        "asset_id": 4,
        "name": "C5",
        "type": "COMPRESSOR",
        "p_nominal": 2500,
        "site": {"address": "20 rue de Paris", "name": "Orsay", "p_max": 18000, "site_id": 1},
    }

    def _get_assets_url(self, manager_id: int, site_id: int) -> str:
        return "{}/managers/{}/sites/{}/assets".format(AppTest.API_URL, manager_id, site_id)

    def _get_asset_url(self, manager_id: int, site_id: int, asset_id: int) -> str:
        return "{}/managers/{}/sites/{}/assets/{}".format(
            AppTest.API_URL, manager_id, site_id, asset_id
        )

    # GET request to /app/assets returns the details of all assets
    # GET request to /app/managers/{manager_id}/sites returns the assets for 1 site
    def test_1_get_all_sites(self):
        manager_id, site_id = 1, 1
        r = requests.get(AppTest.ASSETS_URL)
        r2 = requests.get(self._get_assets_url(manager_id, site_id))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r2.status_code, 200)

    # POST request to /app/managers/{manager_id}/sites/{site_id}/assets to create a new asset
    def test_2_add_new_asset(self):
        manager_id, site_id = 1, 1
        r = requests.post(self._get_assets_url(manager_id, site_id), json=AppTest.ASSET_OBJ)
        self.assertEqual(r.status_code, 201)

    # GET request to /app/managers/{manager_id}/sites/{site_id}/assets/{asset_id} returns an asset
    def test_3_get_an_asset(self):
        manager_id, site_id = 1, 1
        asset_id = AppTest.ASSET_OBJ["asset_id"]
        r = requests.get(self._get_asset_url(manager_id, site_id, asset_id))
        self.assertEqual(r.status_code, 200)
        self.assertDictEqual(r.json(), AppTest.ASSET_OBJ_TEST)

    # PUT request to /app/managers/{manager_id}/sites/{site_id}/assets/{asset_id}
    def test_4_update_existing_asset(self):
        manager_id, site_id = 1, 1

        asset_id = AppTest.ASSET_OBJ["asset_id"]
        r = requests.put(
            self._get_asset_url(manager_id, site_id, asset_id), json=AppTest.UPDATE_ASSET_OBJ
        )
        self.assertEqual(r.status_code, 200)

    # GET request to /app/managers/{manager_id}/sites/{site_id}/assets/{asset_id}
    def test_5_get_new_asset_after_update(self):
        manager_id, site_id = 1, 1
        asset_id = AppTest.UPDATE_ASSET_OBJ["asset_id"]
        r = requests.get(self._get_asset_url(manager_id, site_id, asset_id))
        self.assertEqual(r.status_code, 200)
        self.assertDictEqual(r.json(), AppTest.UPDATE_ASSET_OBJ_TEST)

    # DELETE request to /app/managers/{manager_id}/sites/{site_id}/assets/{asset_id}
    def test_6_delete_asset(self):
        manager_id, site_id = 1, 1
        asset_id = AppTest.UPDATE_ASSET_OBJ["asset_id"]
        r1 = requests.delete(self._get_asset_url(manager_id, site_id, asset_id))
        r2 = requests.get(self._get_asset_url(manager_id, site_id, asset_id))
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(r2.status_code, 404)
