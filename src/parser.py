import sqlparse

from insert_statement import InsertStatement


def parse(query: str):
    query = sqlparse.format(query, strip_comments=True, compact=True)
    statements = sqlparse.parse(query)

    results = []

    for statement in statements:
        statement_parsers = {
            "INSERT": InsertStatement
        }

        results.append(statement_parsers[statement.get_type()].parse(statement))

    return results
