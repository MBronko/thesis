from dataclasses import dataclass, asdict
from enum import StrEnum

from datetime import datetime
import json


class ColumnType(StrEnum):
    STRING = "STRING"
    INT = "INT"
    FLOAT = "FLOAT"
    DATE = "DATE"
    JSON = "JSON"


class ColumnTypeMetadata:
    data_type = {
        ColumnType.STRING: str,
        ColumnType.INT: int,
        ColumnType.FLOAT: float,
        ColumnType.DATE: datetime,
        ColumnType.JSON: str,
    }
    data_parser = {
        ColumnType.STRING: str,
        ColumnType.INT: int,
        ColumnType.FLOAT: float,
        ColumnType.DATE: datetime,
        ColumnType.JSON: json.loads,
    }
    data_serializer = {
        ColumnType.STRING: str,
        ColumnType.INT: str,
        ColumnType.FLOAT: str,
        ColumnType.DATE: lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'),
        ColumnType.JSON: json.dumps,
    }


@dataclass
class Column:
    type: ColumnType

    def __post_init__(self):
        self.type = ColumnType[self.type]


@dataclass
class Table:
    columns: dict[str, Column]
    next_id: int = 1

    def __post_init__(self):
        self.columns = {name: Column(**column) for name, column in self.columns.items()}


@dataclass
class DatabaseStructure:
    tables: dict[str, Table]

    def __post_init__(self):
        self.tables = {name: Table(**table) for name, table in self.tables.items()}

    def to_json(self):
        return json.dumps(asdict(self))
