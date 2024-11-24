from dotenv import load_dotenv
from parser import parse
import os

from src.backend import BackendConnection


def main():
    load_dotenv()

    host = os.environ["REDIS_HOST"]
    port = os.environ["REDIS_PORT"]

    backend_metadata = BackendConnection(host, port)

    # sql = SQL(backend)
    print(backend_metadata.db_structure.to_json())

    statements = parse("""INSERT INTO table1
    VALUES ('test1`', 1), ('test2', 2)""")

    for statement in statements:
        statement.eval(backend_metadata)

    statements = parse("""INSERT INTO table2 t
    VALUES (1.5, '{}'), (2.5, '[]')""")

    for statement in statements:
        statement.eval(backend_metadata)

    statements = parse("""INSERT INTO table1 as t
    VALUES ('test1`', 1), ('test2', 2)""")

    for statement in statements:
        statement.eval(backend_metadata)

    # print(backend.read_db_structure())

    # print(backend.db_structure.tables["table1"].columns["col1"].type)


if __name__ == "__main__":
    main()
