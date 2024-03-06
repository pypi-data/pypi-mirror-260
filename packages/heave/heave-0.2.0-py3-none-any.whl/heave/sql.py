"""Batch SQL operations."""
from sqlalchemy import Connection, MetaData
from sqlalchemy import Table as SqlTable

from heave import Table


def reflect_table(
    connection: Connection, table_name: str, schema: str | None = None
) -> SqlTable:
    """Reflect a table from the database."""
    metadata = MetaData()
    return SqlTable(table_name, metadata, autoload_with=connection, schema=schema)


def insert(connection: Connection, sql_table: SqlTable, data: Table) -> None:
    """Insert data into a table."""
    for row in data.rows:
        connection.execute(sql_table.insert().values(dict(zip(data.header, row))))


def read(connection: Connection, sql_table: SqlTable) -> Table:
    """Read data from a table."""
    result = connection.execute(sql_table.select())
    return Table([tuple(sql_table.columns.keys())] + [row for row in result])
