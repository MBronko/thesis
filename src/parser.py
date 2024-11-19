import sqlparse
from sqlparse.sql import Statement, Token, Identifier, TokenList, Values
from backend import Backend
from src.exceptions import SQLException
from sql_models import Table, InsertStatement
import parser_tools


class SQL:
    def __init__(self, backend: Backend):
        self.backend = backend

    def parse(self, query: str):
        query = sqlparse.format(query, strip_comments=True, compact=True)
        statements = sqlparse.parse(query)

        results = []

        for statement in statements:
            results.append(self.parse_statement(statement))

        return results

    def parse_statement(self, statement: Statement):
        # dml_token = statement.get_token_at_offset(first_token_idx)

        statement_parsers = {
            "INSERT": self.parse_insert,
            "SELECT": self.parse_select,
            "UPDATE": self.parse_update
        }

        return statement_parsers[statement.get_type()](statement)

    def parse_insert(self, statement: Statement):
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

        return InsertStatement(table, values)

    def parse_select(self, statement: Statement):
        pass

    def parse_update(self, statement: Statement):
        pass
