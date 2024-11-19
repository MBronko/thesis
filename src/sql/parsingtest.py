import sqlparse
from sqlparse.sql import Statement


# statements = sqlparse.parse("SELECT * FROM (SELECT * FROM table2) as t WHERE t.col = 'chuj'")
statements = sqlparse.parse("UPDATE table_1 as t1 SET foo = 'new_value' FROM table_2 t2 JOIN table_3 t3 ON t3.id = t2.t3_id WHERE t2.id = t1.t2_id AND t3.bar = True;")

for statement in statements:
    statement: Statement

    print(statement.ttype)
    print(statement.value)
    print(statement.parent)
    print(list(statement.flatten()))
    print(list(statement.get_sublists()))
    # statement: sqlparse.
# print(statements)
# print(statements[0].__class__)
# match parsed:
#     case sqlparse.st