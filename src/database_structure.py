from enum import StrEnum

from datetime import datetime
import json
from typing import Dict, List
from basic_models import Table, Field


class ColumnType(StrEnum):
    STRING = "STRING"
    INT = "INT"
    FLOAT = "FLOAT"
    DATE = "DATE"
    JSON = "JSON"


class ColumnTypeMetadata:
    data_serializer = {
        ColumnType.STRING: str,
        ColumnType.INT: str,
        ColumnType.FLOAT: str,
        ColumnType.DATE: lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'),
        ColumnType.JSON: json.dumps,
    }
    data_deserializer = {
        ColumnType.STRING: str,
        ColumnType.INT: int,
        ColumnType.FLOAT: float,
        ColumnType.DATE: datetime,
        ColumnType.JSON: json.loads,
    }


class Entity:
    def to_dict(self):
        return self.__dict__.copy()

    def to_json(self):
        return json.dumps(self.to_dict())


class ColumnStructure(Entity):
    table_structure: 'TableStructure'
    name: str
    type: ColumnType

    def __init__(self, table_structure: 'TableStructure', column_dict: dict):
        self.table_structure = table_structure
        self.name = column_dict["name"]
        self.type = ColumnType[column_dict["type"]]

    def get_field_object(self, table: Table) -> Field:
        return Field(self.name, self.name, table)

    def get_data_serializer(self):
        return ColumnTypeMetadata.data_serializer[self.type]

    def get_data_deserializer(self):
        return ColumnTypeMetadata.data_deserializer[self.type]

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type
        }


class TableStructure(Entity):
    name: str
    next_id: int
    columns: Dict[str, ColumnStructure]

    def __init__(self, table_dict: dict):
        self.name = table_dict["name"]
        self.next_id = table_dict["next_id"]
        self.columns = {column_dict["name"]: ColumnStructure(self, column_dict) for column_dict in
                        table_dict["columns"]}

    def get_table_object(self) -> Table:
        return Table(self.name, self.name)

    def get_field_objects(self) -> list[Field]:
        table = self.get_table_object()

        return [column_structure.get_field_object(table) for column_structure in self.columns.values()]

    def to_dict(self):
        return {
            "name": self.name,
            "next_id": self.next_id,
            "columns": [column.to_dict() for column in self.columns.values()]
        }

    def get_next_id(self) -> int:
        next_id = self.next_id
        self.next_id += 1
        return next_id


class DatabaseStructure(Entity):
    tables: Dict[str, TableStructure]

    def __init__(self, database_dict: dict):
        self.tables = {table["name"]: TableStructure(table) for table in database_dict["tables"]}

    def to_dict(self):
        return {
            "tables": [table.to_dict() for table in self.tables.values()]
        }
