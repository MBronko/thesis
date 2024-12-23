from sqlparse.sql import Statement, Token, Identifier, Values
from src.exceptions import SQLException
from basic_models import Table
import parser_tools
from dataclasses import dataclass
from src.backend import BackendConnection


@dataclass
class SelectStatement:
    table: Table
    values: list[list]

    @staticmethod
    def parse(statement: Statement):
        idx: int = 0
        token: Token

        idx, token = statement.token_next(idx)

        if token.value != "INTO":
            raise SQLException(f"'INTO' keyword not found in '{statement.value}'")

        idx, token = statement.token_next(idx)

        if not isinstance(token, Identifier):
            raise SQLException(f"input valid table identifier '{statement.value}'")

        name, alias = parser_tools.get_identifier_name(token)

        table = Table(name, alias)

        idx, token = statement.token_next(idx)

        if not isinstance(token, Values):
            raise SQLException(f"input valid values '{statement.value}'")

        values = parser_tools.parse_insert_values(token)

        return SelectStatement(table, values)

    def eval(self, backend_connection: BackendConnection):
        for value_list in self.values:
            columns = backend_connection.get_table_structure(self.table).get_field_objects()

            for column, value in zip(columns, value_list):
                deserializer = backend_connection.get_column_structure(column).get_data_deserializer()

                print(column, value)
                backend_connection.set(column, deserializer(value))
