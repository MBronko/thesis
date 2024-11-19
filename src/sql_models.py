from dataclasses import dataclass


@dataclass
class Identifier:
    name: str
    alias: str


@dataclass
class Table(Identifier):
    pass


@dataclass
class Column(Identifier):
    table: Table


@dataclass
class InsertStatement:
    table: Table
    values: list[list]
