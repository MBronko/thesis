from dotenv import load_dotenv
from parser import parse
import os

from src.backend import BackendConnection


def main():
    load_dotenv()

    host = os.environ["REDIS_HOST"]
    port = os.environ["REDIS_PORT"]

    backend_connection = BackendConnection(host, port)

    statements = parse("""INSERT INTO table1
    VALUES ('test1`', 1), ('test2', 2)""")

    for statement in statements:
        statement.eval(backend_connection)

    statements = parse("""INSERT INTO table2 t
    VALUES (1.5, '{}'), (2.5, '[]')""")

    for statement in statements:
        statement.eval(backend_connection)

    statements = parse("""INSERT INTO table1 as t
    VALUES ('test1`', 1), ('test2', 2)""")

    for statement in statements:
        statement.eval(backend_connection)


if __name__ == "__main__":
    main()
