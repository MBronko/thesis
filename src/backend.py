import redis
import os
import json
from src.database_structure import DatabaseStructure, TableStructure, ColumnStructure, ColumnTypeMetadata
from src.basic_models import Table, Field
from src.exceptions import BackendConnectionException


class BackendConnection:
    def __init__(self, host, port):
        self.connection = redis.Redis(host=host, port=port,
                                      decode_responses=True)
        self.connection.ping()  # throws redis.exceptions.ConnectionError if ping fails

        self.db_structure = self.read_db_structure()


    def initialize_db_structure(self):
        with open("../database_structure.json", "r") as in_file:
            initial_structure = "".join(in_file.readlines())

            self.connection.set(os.environ["DATABASE_METADATA_KEY"], initial_structure)
            return initial_structure


    def read_db_structure(self):
        db_structure_str = self.connection.get(os.environ["DATABASE_METADATA_KEY"])

        if db_structure_str is None or len(db_structure_str) == 0:
            db_structure_str = self.initialize_db_structure()

        db_structure_json = json.loads(db_structure_str)

        return DatabaseStructure(db_structure_json)

    def save_db_structure(self):
        db_structure_json = self.db_structure.to_json()
        self.connection.set(os.environ["DATABASE_METADATA_KEY"], str(db_structure_json))

    def get_table_structure(self, table: Table) -> TableStructure:
        return self.db_structure.tables[table.name]

    def get_column_structure(self, column: Field) -> ColumnStructure:
        return self.get_table_structure(column.table).columns[column.name]

    def get_key(self, field: Field):
        return f"{field.table.name}:{field.name}:{field.table.id}"

    def get(self, column: Field) -> str:
        column_structure = self.get_column_structure(column)

        result = self.connection.get(self.get_key(column))

        deserializer = column_structure.get_data_deserializer()

        return deserializer(result)

    def set(self, column: Field, value) -> None:
        table = column.table

        table_structure = self.get_table_structure(table)
        column_structure = self.get_column_structure(column)

        if table.id is None or table.id == 0:
            table.id = table_structure.get_next_id()
            self.save_db_structure()

        serializer = column_structure.get_data_serializer()

        value = serializer(value)

        self.connection.set(self.get_key(column), value)
