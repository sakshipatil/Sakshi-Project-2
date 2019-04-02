import unittest
import os

from app import app

from mockupdb import MockupDB, go, Command
from pymongo import MongoClient
#from json import dumps

class GetDataSourceTestCase(unittest.TestCase):

    def test_getDataSource(self):
        # arrange
        id = 1
        future = go(self.app.get, f'/edit_user_id/{id}')
        request = self.server.receives(
            Command({'find': 'dataSources', 'filter': {'_id': id}, 'limit': 1, 'singleBatch': True}, flags=4, namespace='app'))
        request.ok(cursor={'id': 0, 'firstBatch': [
            { "first_name" : "Subodh", "last_name" : "Dubey", "email" : "subodh.d@consultadd.in", "address" : "Pune", "description" : "Bhai"  }]})

        # act
        http_response = future()
        # assert
        self.assertIn('http://google.com/rest/api',http_response.get_data(as_text=True))
