import redis
import os
import json
from src.database_structure import DatabaseStructure, Table, Column
from exceptions import BackendConnectionException


class Backend:
    def __init__(self):
        self.connection = redis.Redis(host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"],
                                      decode_responses=True)
        self.connection.ping()  # throws redis.exceptions.ConnectionError if ping fails

        self.db_structure = self.read_db_structure()

    def read_db_structure(self):
        db_structure_str = self.get(os.environ["DATABASE_METADATA_KEY"])

        if db_structure_str is None or len(db_structure_str) == 0:
            raise BackendConnectionException("Can't obtain database metadata")

        db_structure_json = json.loads(db_structure_str)

        return DatabaseStructure(**db_structure_json)

    def save_db_structure(self):
        db_structure_json = self.db_structure.to_json()
        self.set(os.environ["DATABASE_METADATA_KEY"], str(db_structure_json))

    def get(self, key: str) -> str:
        return self.connection.get(key)

    def set(self, key: str, value: str) -> None:
        self.connection.set(key, value)

    def get_next_id(self, table: Table) -> int:
        next_id = table.next_id
        table.next_id += 1
        self.save_db_structure()
        return next_id

    def get_table(self, name: str) -> Table:
        return self.db_structure.tables[name]

    def get_column(self, name) -> Column:
        table, column = name.split(".")
        return self.get_table(table).columns[column]
