from unittest import TestCase

## import the DatabaseHelper class from the src.eam_db_helper.db module
from src.eam_db_helper.db import DatabaseHelper




class CosmosClientMock:
    def __init__(self, uri, key):
        self.results = []

    def get_database_client(self, database):
        return self

    def get_container_client(self, container):
        return self

    def query_items(self, query: str, parameters: list = None, enable_cross_partition_query: bool=False):
        results = self.results
        self.results = []

        return results

    def upsert_item(self, body):        
        self.results.append(body)
        return body
    
    def delete_item(self, item_id, partition_key):
        self.results = None
    

database = DatabaseHelper(
    {
        'account_uri': 'test_uri',
        'key': 'test_key',
        'db_name': 'test_database',
        'container_name': 'test_container'
    }, 
    CosmosClientMock
  )


class TestDatabaseHelper(TestCase):
    def test_get_results(self):
        database.client.results = [{'id': '1'}, {'id': '2'}]
        results = database.get_results('SELECT * FROM c')
        self.assertEqual(results, [{'id': '1'}, {'id': '2'}])

    def test_get_result(self):
        database.client.results = [{'id': '1'}]
        result = database.get_result('SELECT * FROM c')
        self.assertEqual(result, {'id': '1'})

    def test_get_column(self):
        database.client.results = [{'id': '1'}, {'id': '2'}]
        column = database.get_column('id', 'SELECT * FROM c')
        self.assertEqual(column, ['1', '2'])

    def test_delete_item(self):
        database.delete_item('1', '2')
        self.assertEqual(database.client.results, None)

    def test_upsert(self):
        database.upsert({'id': '1', 'partition_key': '2'})
        self.assertEqual(database.client.results, [{'id': '1', 'partition_key': '2'}])