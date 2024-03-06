# Heave

Heave is a CLI tool for batch inserting or updating data into a database.

## Installation

It is recommended to install `heave` using [pipx](https://github.com/pypa/pipx):
```bash
pipx install heave
```

## Usage

`heave [OPTIONS] COMMAND [ARGS]...`

Create a connection to a PostgreSQL database.

Defaults to the `postgres` database on `localhost` with the `postgres` user.
Pass alternate connection parameters as options.
You can save yourself some typing by setting the environment variables `PGDATABASE`, 
`PGHOST`, `PGPORT` and/or `PGUSER` to appropriate values.
It is also convenient to have a [.pgpass](https://www.postgresql.org/docs/current/libpq-pgpass.html) file 
to avoid regularly having to type in passwords.

#### Options

`-h`, `--host TEXT (default: localhost)`
- Host name of the database.

`-p`, `--port INTEGER (default: 5432)`
- Port number at which the database is listening.

`-U`, `--username TEXT`
- Username to connect as.

`-d`, `--dbname TEXT (default: postgres)`
- Name of the database to connect to.

#### Examples

```bash
heave --host myhost --port 5433 --username myuser --dbname mydb
```

### heave insert

`heave insert --table TEXT <file>`

Insert data from a file into a table.

#### Options

`-t`, `--table TEXT`
- Name of the table to insert into. Required.

#### Examples

```bash
heave insert --table mytable data.csv
```

### heave read

`heave read --table TEXT <file>`

Read data from an SQL table and write it to a file.

#### Options

`-t`, `--table TEXT`
- Name of the table to read from. Required.

#### Examples

```bash
heave read --table mytable data.csv
```

## Supported Formats

Currently, Heave only supports extracting data from CSV files and loading it into a PostgreSQL database.

### Sources

Supported data sources include:

* CSV files: `.csv`

### Databases

Supported target databases include:

* PostgreSQL

## Examples

...

## Contributing

Contributions are welcome! Pick an existing issue or create a new one.
Then follow the steps in [CONTRIBUTING.md](/CONTRIBUTING.md) to make your change.`