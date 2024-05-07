import dataclasses

from models.models import Hosts
from pymongo import MongoClient


@dataclasses.dataclass
class MongoHostsManager:
    """
    Class to manage Hosts data in a MongoDB database.
    """

    client: MongoClient  # Database client connection

    def __init__(self, host: str = "0.0.0.0", port: int = 27017, database_name: str = "database",
                 collection_name: str = "hosts"):
        """
        Initializes the MongoHostsManager with connection details.

        Args:
            host (str, optional): MongoDB host address. Defaults to "localhost".
            port (int, optional): MongoDB port number. Defaults to 27017.
            database_name (str, optional): Database name. Defaults to "database".
            collection_name (str, optional): Collection name. Defaults to "hosts".
        """
        self.client = MongoClient(host, port)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def search(self, hostname: str) -> dict:
        """
        Searches for a host by its hostname.

        Args:
            hostname (str): The hostname to search for.

        Returns:
            dict: A dictionary representing the found host data or None if not found.
        """
        return self.collection.find_one({"hostname": hostname})

    def store(self, data: dict):
        """
        Stores or updates host data in the database.

        Args:
            data (dict): A dictionary containing host information.
        """
        found = self.search(data["hostname"])
        if found:
            _id = found["_id"]
            del found["_id"]
            merged = Hosts(**data).merge_hosts(Hosts(**found))
            self.collection.find_one_and_update({"_id": _id}, {"$set": dataclasses.asdict(merged)})
        else:
            self.collection.insert_one(data)

