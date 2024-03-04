import unittest
import requests_mock
from src.andromedaClient import AndromedaClient

# you need to install requests-mock to run these tests
# pip install requests-mock
# run the tests with the following command: python -m unittest tests/test.py from root directory


class TestAndromedaClient(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://localhost:8000'
        self.username = 'testuser'
        self.password = 'testpassword'
        self.client = AndromedaClient(self.base_url, self.username, self.password)

    @requests_mock.Mocker()
    def test_get(self, m):
        url_path = '/test'
        m.get(self.base_url + url_path, json=[{'key': 'value'}])
        response = self.client.get(url_path)
        self.assertEqual(response, [{'key': 'value'}])

    def callback(request, context): 
        print("request path: ", request.path) 

    @requests_mock.Mocker()
    def test_paginate_get(self, m):
        url_path_base = '/test'
        
        m.get(self.base_url + url_path_base + "?page=0", json=[{'key': 'value'} for i in range(1000)])
        m.get(self.base_url + url_path_base + "?page=1", json=[{'key': 'value'}])

        response = self.client.paginate('get', self.base_url + url_path_base)
        self.assertEqual(response, [{'key': 'value'} for i in range(1001)])

    @requests_mock.Mocker()
    def test_paginate_post(self, m):
        url_path_base = '/test'
        
        m.post(self.base_url + url_path_base + "?page=0", json=[{'key': 'value'} for i in range(1000)])
        m.post(self.base_url + url_path_base + "?page=1", json=[{'key': 'value'}])

        response = self.client.paginate('post', self.base_url + url_path_base, payload={'key': 'value'})
        self.assertEqual(response, [{'key': 'value'} for i in range(1001)])

    def test_divide_chunks(self):
        l = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        chunks = list(self.client.divide_chunks(l, 3))
        self.assertEqual(chunks, [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

if __name__ == '__main__':
    unittest.main()