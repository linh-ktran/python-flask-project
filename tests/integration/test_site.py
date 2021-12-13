import unittest

import requests

BASE_URL = "http://127.0.0.1:5000/app"
SITES_URL = "{}/sites".format(BASE_URL)


class AppTest(unittest.TestCase):

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
        """Return the ULR for list of sites"""
        return "{}/managers/{}/sites".format(BASE_URL, manager_id)

    def _get_site_url(self, manager_id: int, site_id: int) -> str:
        """Return the ULR for a site"""
        return "{}/managers/{}/sites/{}".format(BASE_URL, manager_id, site_id)

    def test_1_get_sites(self):
        """
        GET request to /app/sites returns the details of all sites
        GET request to /app/managers/{manager_id}/sites returns the sites for 1 manager
        GET request to /app/managers/{manager_id}/sites/{site_id} returns a specific site
        """
        manager_id, site_id = 1, 1
        response = requests.get(SITES_URL)
        self.assertEqual(response.status_code, 200)
        response = requests.get(self._get_sites_url(manager_id))
        self.assertEqual(response.status_code, 200)
        response = requests.get(self._get_site_url(manager_id, site_id))
        self.assertEqual(response.status_code, 200)

    def test_2_add_new_site(self):
        """
        POST request to /app/managers/{manager_id}/sites
        to create a new site check if the new site is actually added
        """
        manager_id = 1
        site_id = AppTest.SITE_OBJ["site_id"]
        response = requests.post(self._get_sites_url(manager_id), json=AppTest.SITE_OBJ)
        self.assertEqual(response.status_code, 201)
        response = requests.get(self._get_site_url(manager_id, site_id))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), AppTest.SITE_OBJ_TEST)

    def test_3_update_existing_site(self):
        """
        PUT request to /app/managers/{manager_id}/sites/{site_id}
        to update an existing site and check if the new site is actually updated
        """
        manager_id = 1
        site_id = AppTest.SITE_OBJ["site_id"]
        response = requests.put(
            self._get_site_url(manager_id, site_id), json=AppTest.UPDATE_SITE_OBJ
        )
        self.assertEqual(response.status_code, 200)
        response = requests.get(self._get_site_url(manager_id, site_id))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), AppTest.UPDATE_SITE_OBJ_TEST)

    def test_4_delete_site(self):
        """
        DELETE request to /app/managers/{manager_id}/sites/{site_id}
        to delete a site and check if the new asset is actually deleted
        """
        manager_id = 1
        site_id = AppTest.UPDATE_SITE_OBJ["site_id"]
        response = requests.delete(self._get_site_url(manager_id, site_id))
        self.assertEqual(response.status_code, 200)
        response = requests.get(self._get_site_url(manager_id, site_id))
        self.assertEqual(response.status_code, 404)
