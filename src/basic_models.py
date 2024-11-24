from dataclasses import dataclass


@dataclass
class Identifier:
    name: str
    alias: str


@dataclass
class Table(Identifier):
    id: int = 0


@dataclass
class Field(Identifier):
    table: Table
    value: any = None
