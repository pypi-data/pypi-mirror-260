import logging
from azure.cosmos import CosmosClient
from functools import lru_cache

logger = logging.getLogger("azure")
logger.setLevel(logging.WARN)


# @lru_cache(maxsize=5)
class DatabaseHelper:
    def __init__(self, cosmos_metadata, connection=CosmosClient):
        
        self.cosmos_metadata = {
            'account_uri': cosmos_metadata['account_uri'],
            'key': cosmos_metadata['key'],
            'db_name': cosmos_metadata['db_name'],
            'container_name': cosmos_metadata['container_name']            
        }
        self.client = connection(
            self.cosmos_metadata["account_uri"], self.cosmos_metadata["key"]
        )
        self.db = self.client.get_database_client(self.cosmos_metadata["db_name"])
        self.container = self.db.get_container_client(self.cosmos_metadata["container_name"])


    # return all query results as a list
    def get_results(self, query: str, parameters: list = [], enable_cross_partition=False) -> list:
        try:
            items = self.container.query_items(query=query, parameters=parameters, enable_cross_partition_query=enable_cross_partition)
            return list(items)
        except Exception as e:
            logger.error(f"Error getting results: {e}")
            return []


    # return a single result as a dict
    def get_result(self, query: str, parameters: list = [], enable_cross_partition=False) -> dict:
        try:
            items = self.container.query_items(query=query, parameters=parameters, enable_cross_partition_query=enable_cross_partition)
            itemsList = list(items)

            if len(itemsList) > 0:
                return itemsList[0]
            return {}
        except Exception as e:
            logger.error(f"Error getting result: {e}")
            return {}


    # return a list of a single column from the query results
    def get_column(self, column_name: str, query: str, parameters: list = []) -> list:
        try:
            items = self.container.query_items(query=query, parameters=parameters)
            return [item[column_name] for item in items]
        except Exception as e:
            logger.error(f"Error getting column: {e}")
            return []


    # delete an item by id and partition key
    def delete_item(self, item_id: str, pk: str) -> None:
        self.container.delete_item(item_id, partition_key=pk)


    def upsert(self, item: dict) -> dict:
        return self.container.upsert_item(item)

