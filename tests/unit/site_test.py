import unittest
import requests


class AppTest(unittest.TestCase):
    API_URL = "http://127.0.0.1:5000/app"
    SITES_URL = "{}/sites".format(API_URL)

    SITE_OBJ = {
        "site_id": 4,
        "name": "Newsite",
        "address": "30 ABC street",
        "p_max": 20000,
    }

    SITE_OBJ_TEST = {
        "site_id": 4,
        "name": "Newsite",
        "address": "30 ABC street",
        "p_max": 20000,
        "assets": [],
        "manager": {"fname": "Nicolas", "lname": "Plain", "manager_id": 1},
    }

    UPDATE_SITE_OBJ = {
        "site_id": 4,
        "name": "California",
        "address": "30 Carlos street",
    }

    UPDATE_SITE_OBJ_TEST = {
        "site_id": 4,
        "name": "California",
        "address": "30 Carlos street",
        "p_max": 20000,
        "assets": [],
        "manager": {"fname": "Nicolas", "lname": "Plain", "manager_id": 1},
    }

    def _get_sites_url(self, manager_id: int) -> str:
        return "{}/managers/{}/sites".format(AppTest.API_URL, manager_id)

    def _get_site_url(self, manager_id: int, site_id: int) -> str:
        return "{}/managers/{}/sites/{}".format(AppTest.API_URL, manager_id, site_id)

    # GET request to /app/sites returns the details of all sites
    # GET request to /app/managers/{manager_id}/sites returns the sites for 1 manager
    def test_1_get_all_sites(self):
        manager_id = 1
        r = requests.get(AppTest.SITES_URL)
        r2 = requests.get(self._get_sites_url(manager_id))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r2.status_code, 200)

    # POST request to /app/managers/{manager_id}/sites to create a new site
    def test_2_add_new_site(self):
        manager_id = 1
        r = requests.post(self._get_sites_url(manager_id), json=AppTest.SITE_OBJ)
        self.assertEqual(r.status_code, 201)

    # GET request to /app/managers/{manager_id}/sites/{site_id} returns a site
    def test_3_get_a_site(self):
        manager_id = 1
        site_id = AppTest.SITE_OBJ["site_id"]
        r = requests.get(self._get_site_url(manager_id, site_id))
        self.assertEqual(r.status_code, 200)
        self.assertDictEqual(r.json(), AppTest.SITE_OBJ_TEST)

    # PUT request to /app/managers/{manager_id}/sites/{site_id}
    def test_4_update_existing_manager(self):
        manager_id = 1
        site_id = AppTest.SITE_OBJ["site_id"]
        r = requests.put(self._get_site_url(manager_id, site_id), json=AppTest.UPDATE_SITE_OBJ)
        self.assertEqual(r.status_code, 200)

    # GET request to /app/managers/{manager_id}/sites/{site_id}
    def test_5_get_new_site_after_update(self):
        manager_id = 1
        site_id = AppTest.UPDATE_SITE_OBJ["site_id"]
        r = requests.get(self._get_site_url(manager_id, site_id))
        self.assertEqual(r.status_code, 200)
        self.assertDictEqual(r.json(), AppTest.UPDATE_SITE_OBJ_TEST)

    # DELETE request to /app/managers/{manager_id}/sites/{site_id}
    def test_6_delete_site(self):
        manager_id = 1
        site_id = AppTest.UPDATE_SITE_OBJ["site_id"]
        r1 = requests.delete(self._get_site_url(manager_id, site_id))
        r2 = requests.get(self._get_site_url(manager_id, site_id))
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(r2.status_code, 404)
