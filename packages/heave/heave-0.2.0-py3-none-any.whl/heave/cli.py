"""Heave CLI."""


import click
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from heave import file, sql


def connect(
    context: click.Context,
    dialect: str,
    database: str,
    host: str = "",
    port: str = "",
    user: str = "",
    driver: str = "",
) -> None:
    """Initialize a database connection and add it to the click context.

    Generates a database URL from the parameters and creates an SQLAlchemy engine.
    Validates the connection prompting for a password if necessary.
    Adds a connection to the click context as a resource.
    Heavily inspired by pgcli: https://github.com/dbcli/pgcli/blob/main/pgcli/main.py

    :param context: Click context.
    :param dialect: Database dialect.
    :param driver: Database driver.
    :param database: Database name.
    :param host: Database host.
    :param user: Database user.
    :param port: Database port.
    """
    driver = "+" + driver if driver else ""
    host = "@" + host if user else host
    port = ":" + port if port else port
    db_url = f"{dialect}{driver}://{user}{host}{port}/{database}"
    engine = create_engine(db_url)
    try:
        try:
            engine.connect()
        except OperationalError as e:
            if user and "no password supplied" in str(e):
                password = click.prompt(f"Password for {user}", hide_input=True)
                db_url = f"{dialect}{driver}://{user}{password}{host}{port}/{database}"
                engine = create_engine(db_url)
                engine.connect()
            else:
                click.secho(str(e), err=True, fg="red")
                exit(1)
    except Exception as e:
        click.secho(str(e), err=True, fg="red")
        exit(1)
    context.obj = context.with_resource(engine.begin())
    click.echo(f"Connected to {database}!")


@click.group()
@click.option(
    "-h",
    "--host",
    default="localhost",
    envvar="PGHOST",
    help="Host address of the postgres database.",
)
@click.option(
    "-p",
    "--port",
    default=5432,
    help="Port number at which the postgres instance is listening.",
    envvar="PGPORT",
    type=click.INT,
)
@click.option(
    "-U",
    "--username",
    default="",
    help="Username to connect to the postgres database.",
    envvar="PGUSER",
)
@click.option(
    "-d",
    "--dbname",
    default="postgres",
    help="Database name to connect to.",
    envvar="PGDATABASE",
)
@click.pass_context
def cli(
    ctx,
    host: str,
    port: int,
    username: str,
    dbname: str,
):
    """Heave CLI."""
    # default to postgres connection parameters
    dialect = "postgresql"
    driver = "psycopg"
    connect(ctx, dialect, dbname, host, str(port), username, driver)


@cli.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("-t", "--table", required=True, help="Table to insert into.")
@click.option("-s", "--schema", help="Table schema name.")
@click.pass_obj
def insert(obj, path: str, table: str, schema: str | None):
    """Insert data from a file into a table."""
    data = file.read_csv(path)
    sql_table = sql.reflect_table(obj, table, schema)
    sql.insert(obj, sql_table, data)
    click.echo(f"Inserted rows into {sql_table.name}.")


@cli.command()
@click.argument("path", type=click.Path(exists=False))
@click.option("-t", "--table", required=True, help="Table to read.")
@click.option("-s", "--schema", help="Table schema name.")
@click.pass_obj
def read(obj, path: str, table: str, schema: str | None):
    """Read data from a table and write it to a file."""
    sql_table = sql.reflect_table(obj, table, schema)
    data = sql.read(obj, sql_table)
    file.write_csv(data, path)
    click.echo(f"Wrote data to {path}.")
