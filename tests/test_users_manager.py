import unittest

import requests

BASE_URL = "http://127.0.0.1:5000/app"
MANAGERS_URL = "{}/managers".format(BASE_URL)


class AppTest(unittest.TestCase):

    FIRST_MANAGER = {
        "manager_id": 1, "fname": "Nicolas", "lname": "Plain",
        "sites": [{"site_id": 1}, {"site_id": 2}]
    }
    NEW_MANAGER = {
        "manager_id": 7, "fname": "Luca", "lname": "Rava",
        "sites": [{"site_id": 1}, {"site_id": 2}]
    }
    BAD_MANAGER = {"fname": "Luca", "lname": "Rava", "sites": [{"site_id": 12}]}

    MANAGER = {"manager_id": 10, "fname": "Lu", "lname": "Ra"}
    UPDATE_MANAGER = {"manager_id": 10, "fname": "Lucas", "lname": "Ravan"}
    UPDATE_MANAGER_CHECK = {"manager_id": 10, "fname": "Lucas", "lname": "Ravan", "sites": []}

    def _get_manager_url(self, manager_id: int) -> str:
        """Return the ULR for a manager"""
        return "{}/manager/{}".format(BASE_URL, manager_id)

    def test_get_managers(self):
        """
        GET request to /app/managers returns the details of all manager
        """
        response = requests.get(MANAGERS_URL)
        self.assertEqual(response.status_code, 200)

    def test_get_a_manager(self):
        """
        GET request to /app/managers/{manager_id} returns a manager
        """
        manager_id = AppTest.FIRST_MANAGER["manager_id"]
        response = requests.get(self._get_manager_url(manager_id=manager_id))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), AppTest.FIRST_MANAGER)

    def test_add_valid_manager(self):
        """
        POST request to /app/managers to create a new manager with associated sites
        """
        manager_id = AppTest.NEW_MANAGER["manager_id"]
        response = requests.post(MANAGERS_URL, json=AppTest.NEW_MANAGER)
        self.assertEqual(response.status_code, 201)
        # Check if the new manager is actually added
        response = requests.get(self._get_manager_url(manager_id=manager_id))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), AppTest.NEW_MANAGER)

    def test_add_invalid_manager(self):
        """
        POST request to /app/managers to create a new manager
        """
        response = requests.post(MANAGERS_URL, json=AppTest.BAD_MANAGER)
        self.assertEqual(response.status_code, 404)

    def test_update_an_existing_manager(self):
        """
        PUT request to /app/managers/manager_id to update a manager
        """
        manager_id = AppTest.UPDATE_MANAGER["manager_id"]
        requests.post(MANAGERS_URL, json=AppTest.MANAGER)
        response = requests.put(self._get_manager_url(manager_id), json=AppTest.UPDATE_MANAGER)
        self.assertEqual(response.status_code, 200)

        # Check if the new manager is actually updated
        response = requests.get(self._get_manager_url(manager_id=manager_id))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), AppTest.UPDATE_MANAGER_CHECK)

    def test_delete_manager(self):
        """
        DELETE request to /app/managers/manager_id to delete a manager
        """
        manager_id = AppTest.NEW_MANAGER["manager_id"]
        requests.post(MANAGERS_URL, json=AppTest.NEW_MANAGER)
        response = requests.delete(self._get_manager_url(manager_id=manager_id))
        self.assertEqual(response.status_code, 200)

        # Check if the manager is actually deleted
        response = requests.get(self._get_manager_url(manager_id=manager_id))
        self.assertEqual(response.status_code, 404)
        response = requests.delete(self._get_manager_url(manager_id=manager_id))
        self.assertEqual(response.status_code, 404)
