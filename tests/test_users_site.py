import unittest

import requests

BASE_URL = "http://127.0.0.1:5000/app"
SITES_URL = "{}/sites".format(BASE_URL)


class AppTest(unittest.TestCase):

    SITE = {
        "site_id": 11,
        "address": "20 rue de Paris",
        "name": "Orsay",
        "p_max": 18000,
    }

    SITE_CHECK = {
        "site_id": 11,
        "address": "20 rue de Paris",
        "name": "Orsay",
        "p_max": 18000,
        "assets": [],
    }

    NEW_SITE = {
        "site_id": 4,
        "name": "Newsite",
        "address": "30 ABC street",
        "p_max": 7000,
    }

    NEW_SITE_CHECK = {
        "site_id": 4,
        "name": "Newsite",
        "address": "30 ABC street",
        "p_max": 7000,
        "assets": [],
    }

    SITE_WITH_MANAGERS = {
        "site_id": 5,
        "name": "Newsite",
        "address": "30 ABC street",
        "p_max": 7000,
        "managers": [{"manager_id": 3}, {"manager_id": 2}],
    }

    SITE_WITH_MANAGERS_CHECK = {
        "site_id": 5,
        "name": "Newsite",
        "address": "30 ABC street",
        "p_max": 7000,
        "assets": [],
    }

    UPDATE_SITE = {
        "site_id": 4,
        "name": "California",
        "address": "30 Carlos street",
    }

    UPDATE_SITE_CHECK = {
        "site_id": 4,
        "name": "California",
        "address": "30 Carlos street",
        "p_max": 7000,
        "assets": [],
    }

    UPDATE_BAD_SITE = {
        "site_id": 1,
        "p_max": 2000,
    }

    def _get_site_url(self, site_id: int) -> str:
        """Return the ULR for a site"""
        return "{}/site/{}".format(BASE_URL, site_id)

    def test_get_sites(self):
        """
        GET request to /app/sites returns the details of all sites
        """
        response = requests.get(SITES_URL)
        self.assertEqual(response.status_code, 200)

    def test_get_a_site(self):
        """
        GET request to /app/site/{site_id} returns a specific site
        """
        site_id = AppTest.SITE["site_id"]
        requests.post(SITES_URL, json=AppTest.SITE)
        response = requests.get(self._get_site_url(site_id=site_id))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), AppTest.SITE_CHECK)

    def test_add_a_site(self):
        """
        POST request to /app/managers/{manager_id}/sites to create a new site
        """
        site_id = AppTest.NEW_SITE["site_id"]
        response = requests.post(SITES_URL, json=AppTest.NEW_SITE)
        self.assertEqual(response.status_code, 201)

        # Check if the new site is actually added
        response = requests.get(self._get_site_url(site_id=site_id))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), AppTest.NEW_SITE_CHECK)

    def test_add_a_site_with_managers(self):
        """
        POST request to /app/managers/{manager_id}/sites to create a new site
        with associated existing managers
        """
        site_id = AppTest.SITE_WITH_MANAGERS["site_id"]
        response = requests.post(SITES_URL, json=AppTest.SITE_WITH_MANAGERS)
        self.assertEqual(response.status_code, 201)

        # Check if the new site is actually added
        response = requests.get(self._get_site_url(site_id=site_id))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), AppTest.SITE_WITH_MANAGERS_CHECK)

    def test_update_existing_site(self):
        """
        PATCH request to /app/managers/{manager_id}/sites/{site_id}
        to update an existing site
        """
        requests.post(SITES_URL, json=AppTest.NEW_SITE)
        site_id = AppTest.UPDATE_SITE["site_id"]
        response = requests.patch(self._get_site_url(site_id=site_id), json=AppTest.UPDATE_SITE)
        self.assertEqual(response.status_code, 200)

        # Check if the new site is actually updated
        response = requests.get(self._get_site_url(site_id=site_id))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), AppTest.UPDATE_SITE_CHECK)

    def test_update_invalid_site(self):
        """
        PATCH request to /app/managers/{manager_id}/sites/{site_id}
        to update an existing site
        """
        requests.post(SITES_URL, json=AppTest.NEW_SITE)
        site_id = AppTest.UPDATE_BAD_SITE["site_id"]
        response = requests.patch(
            self._get_site_url(site_id=site_id), json=AppTest.UPDATE_BAD_SITE
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_site(self):
        """
        DELETE request to /app/managers/{manager_id}/sites/{site_id} to delete a site
        """
        site_id = AppTest.NEW_SITE["site_id"]
        requests.post(SITES_URL, json=AppTest.NEW_SITE)
        response = requests.delete(self._get_site_url(site_id=site_id))
        self.assertEqual(response.status_code, 200)

        # Check if the new asset is actually deleted
        response = requests.get(self._get_site_url(site_id=site_id))
        self.assertEqual(response.status_code, 404)
