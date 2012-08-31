"""
Contains functions and classes for parsing and storing the results of a `net use` command on
Windows. This table describes what the mounted UNC paths.
"""


from copy import deepcopy

from win_unc.internal.parsing import drop_while, take_while, first, rfirst, not_
from win_unc.internal.shell import run


EMPTY_TABLE_INDICATOR = 'There are no entries in the list.'
LAST_TABLE_LINE = 'The command completed successfully.'


def is_line_separator(line):
    return line and all(char == '-' for char in line)


def get_columns(lines):
    header_iter = take_while(not_(is_line_separator), lines)
    headings = rfirst(lambda x: x and x[0].isalpha(), header_iter)

    names = headings.split()
    starts = [headings.index(name) for name in names]
    ends = [right - 1 for right in starts[1:]] + [None]

    return [NetUseColumn(name, start, end)
            for name, start, end in zip(names, starts, ends)]


def get_body(lines):
    bottom = drop_while(not_(is_line_separator), lines)
    is_last_line = lambda x: x and x != LAST_TABLE_LINE
    return (take_while(is_last_line, bottom[1:])
            if len(bottom) > 1
            else [])


class NetUseColumn(object):
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end

    def extract(self, string):
        return string[self.start:self.end].strip()

    def __repr__(self):
        return '<{cls} "{name}": {start}-{end}>'.format(
            cls=self.__class__.__name__,
            name=self.name,
            start=self.start,
            end=self.end)


class NetUseRow(object):
    def __init__(self, string, columns):
        self._fields = {column.name: column.extract(string)
                        for column in columns}

    def __getitem__(self, key):
        return self._fields[key]

    def __repr__(self):
        return '<{cls}: {fields}>'.format(
            cls=self.__class__.__name__,
            fields=self._fields)


class NetUseTable(object):
    def __init__(self):
        self.rows = []

    def add_row(self, row):
        self.rows.append(row)

    def get_column(self, column):
        return [row[column] for row in self.rows]

    def get_mounted_paths(self):
        return self.get_column('Remote')

    def get_mounted_drives(self):
        return self.get_column('Local')


def parse_net_use_table(string):
    lines = [line.rstrip() for line in string.split('\n')]

    table_columns = get_columns(lines)
    table_body = get_body(lines)

    table = NetUseTable()
    for this_row, next_row in zip(table_body, table_body[1:] + [None]):
        if next_row and next_row.startswith(' '):
            columns = deepcopy(table_columns)
            columns[-2].end = len(this_row)
            columns[-1].start = len(this_row) + 1

            table.add_row(NetUseRow(this_row + ' ' + next_row.strip(), columns))
        elif not this_row.startswith(' '):
            table.add_row(NetUseRow(this_row, table_columns))

    return table


def get_net_use_table_from_string(string):
    if EMPTY_TABLE_INDICATOR in string:
        return NetUseTable()
    else:
        return parse_net_use_table(string)
