from dotenv import load_dotenv
from backend import Backend
from src.parser import SQL

def main():
    load_dotenv()

    backend = Backend()

    sql = SQL(backend)
    sql.parse("""INSERT INTO table1
    VALUES ('test1`', 1), ('test2', 2)""")

    sql.parse("""INSERT INTO table2 t
    VALUES (1.5, '{}'), (2.5, '[]')""")

    sql.parse("""INSERT INTO table1 as t
    VALUES ('test1`', 1), ('test2', 2)""")

    # print(backend.read_db_structure())

    # print(backend.db_structure.tables["table1"].columns["col1"].type)


if __name__ == "__main__":
    main()
