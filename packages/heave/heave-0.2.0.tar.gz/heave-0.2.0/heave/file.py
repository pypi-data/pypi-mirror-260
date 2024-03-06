"""Extract tabular data into a custom Table object."""
import csv


class Table:
    """Two-dimensional data with a header."""

    def __init__(self, data: list[tuple[str, ...]]):
        """Initialise table with data."""
        self._data = data

    @property
    def header(self) -> tuple[str, ...]:
        """Return the table header."""
        return self._data[0]

    @property
    def rows(self):
        """Yield the table rows."""
        for row in self._data[1:]:
            yield row

    def __eq__(self, other):
        """Return True if the data is equal."""
        return self._data == other._data


def read_csv(file: str) -> Table:
    """Read a csv file and return a Table."""
    with open(file, "r", newline="") as f:
        reader = csv.reader(f)
        data = [tuple(row) for row in reader]
    return Table(data)


def write_csv(data: Table, file: str) -> None:
    """Write a Table to a csv file."""
    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        rows = [data.header, *data.rows]
        writer.writerows(rows)
