import unittest

import requests

BASE_URL = "http://127.0.0.1:5000/app"
MANAGERS_URL = "{}/managers".format(BASE_URL)


class AppTest(unittest.TestCase):

    MANAGER_OBJ = {"manager_id": 3, "fname": "Luca", "lname": "Rava"}
    MANAGER_OBJ_TEST = {"manager_id": 3, "fname": "Luca", "lname": "Rava", "sites": []}
    UPDATE_MANAGER_OBJ = {"manager_id": 3, "fname": "Lucas"}
    UPDATE_MANAGER_OBJ_TEST = {"manager_id": 3, "fname": "Lucas", "lname": "Rava", "sites": []}

    def _get_manager_url(self, manager_id: int) -> str:
        """Return the ULR for a manager"""
        return "{}/{}".format(MANAGERS_URL, manager_id)

    def test_1_get_managers(self):
        """
        GET request to /app/managers returns the details of all manager
        GET request to /app/managers/manager_id returns a manager
        """
        manager_id = 1
        response = requests.get(MANAGERS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        response = requests.get(self._get_manager_url(manager_id=manager_id))
        self.assertEqual(response.status_code, 200)

    def test_2_add_new_manager(self):
        """
        POST request to /app/managers to create a new manager
        and check if the new manager is actually added
        """
        manager_id = AppTest.MANAGER_OBJ["manager_id"]
        response = requests.post(MANAGERS_URL, json=AppTest.MANAGER_OBJ)
        self.assertEqual(response.status_code, 201)
        response = requests.get(self._get_manager_url(manager_id=manager_id))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), AppTest.MANAGER_OBJ_TEST)

    def test_3_update_existing_manager(self):
        """
        PUT request to /app/managers/manager_id
        GET request to /app/managers/manager_id
        to update un manager and check if the new manager is actually updated
        """
        manager_id = AppTest.MANAGER_OBJ["manager_id"]
        response = requests.put(self._get_manager_url(manager_id), json=AppTest.UPDATE_MANAGER_OBJ)
        self.assertEqual(response.status_code, 200)
        response = requests.get(self._get_manager_url(manager_id=manager_id))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), AppTest.UPDATE_MANAGER_OBJ_TEST)

    def test_4_delete_manager(self):
        """
        DELETE request to /app/managers/manager_id
        to delete an asset and check if the asset is actually deleted
        """
        manager_id = AppTest.UPDATE_MANAGER_OBJ["manager_id"]
        bad_manager_id = AppTest.UPDATE_MANAGER_OBJ["manager_id"]
        response = requests.delete(self._get_manager_url(manager_id=manager_id))
        self.assertEqual(response.status_code, 200)
        response = requests.get(self._get_manager_url(manager_id=manager_id))
        self.assertEqual(response.status_code, 404)
        response = requests.delete(self._get_manager_url(manager_id=bad_manager_id))
        self.assertEqual(response.status_code, 404)
