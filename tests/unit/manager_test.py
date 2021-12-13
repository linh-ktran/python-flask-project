import unittest

import requests


class AppTest(unittest.TestCase):
    API_URL = "http://127.0.0.1:5000/app"
    MANAGERS_URL = "{}/managers".format(API_URL)

    MANAGER_OBJ = {"manager_id": 3, "fname": "Luca", "lname": "Rava"}

    MANAGER_OBJ_TEST = {"manager_id": 3, "fname": "Luca", "lname": "Rava", "sites": []}

    UPDATE_MANAGER_OBJ = {
        "manager_id": 3,
        "fname": "Lucas",
    }

    UPDATE_MANAGER_OBJ_TEST = {"manager_id": 3, "fname": "Lucas", "lname": "Rava", "sites": []}

    def _get_manager_url(self, manager_id: int) -> str:
        return "{}/{}".format(AppTest.MANAGERS_URL, manager_id)

    # GET request to /app/managers returns the details of all manager
    def test_1_get_all_managers(self):
        r = requests.get(AppTest.MANAGERS_URL)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 2)

    # POST request to /app/managers to create a new manager
    def test_2_add_new_manager(self):
        r = requests.post(AppTest.MANAGERS_URL, json=AppTest.MANAGER_OBJ)
        self.assertEqual(r.status_code, 201)

    # GET request to /app/managers/manager_id returns a manager
    def test_3_get_a_manager(self):
        manager_id = AppTest.MANAGER_OBJ["manager_id"]
        r = requests.get(self._get_manager_url(manager_id))
        self.assertEqual(r.status_code, 200)
        self.assertDictEqual(r.json(), AppTest.MANAGER_OBJ_TEST)

    # PUT request to /app/managers/manager_id
    def test_4_update_existing_manager(self):
        manager_id = AppTest.MANAGER_OBJ["manager_id"]
        r = requests.put(self._get_manager_url(manager_id), json=AppTest.UPDATE_MANAGER_OBJ)
        self.assertEqual(r.status_code, 200)

    # GET request to /app/managers/manager_id
    def test_5_get_new_manager_after_update(self):
        manager_id = AppTest.UPDATE_MANAGER_OBJ["manager_id"]
        r = requests.get(self._get_manager_url(manager_id))
        self.assertEqual(r.status_code, 200)
        self.assertDictEqual(r.json(), AppTest.UPDATE_MANAGER_OBJ_TEST)

    # DELETE request to /app/managers/manager_id
    def test_6_delete_manager(self):
        manager_id = AppTest.UPDATE_MANAGER_OBJ["manager_id"]
        r1 = requests.delete(self._get_manager_url(manager_id))
        r2 = requests.get(self._get_manager_url(manager_id))
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(r2.status_code, 404)
