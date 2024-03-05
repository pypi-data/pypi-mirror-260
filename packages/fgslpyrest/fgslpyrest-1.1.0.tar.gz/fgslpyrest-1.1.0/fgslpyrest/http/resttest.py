import unittest
from fgslpyrest.http.Rest import Rest
import json

class TestRestMethods(unittest.TestCase):

    def testGet(self):
        rest = Rest()
        response = rest.doGet([],"https://time.is/pt_br/UTC",200,True)
        self.assertTrue(response.find("German"))

        response = rest.doGet([],"https://time.is/pt_br/UTC",[200,201],True)
        self.assertTrue(response.find("German"))

    def testGetReturningJson(self):
        rest = Rest()
        response = rest.doGet([],"https://reqres.in/api/users/2",200)
        user = json.loads(response)
        self.assertTrue(user["data"]["email"] is not None)

if __name__ == '__main__':
    unittest.main()