#!/usr/bin/env python

import csv
from collections import namedtuple


def write_csv(outfile, rows, delimiter=',', headers=[], encoding='utf-8'):
    """Creates a csv file with a given name from the given rows
    TODO: Add support for writing out namedtuples with headers
    Args:
        string     outfile:    the file to writeout
        collection rows:       a collection of rows, each a collection
                               (eg, a list of lists)

        OPTIONAL:
        string      delimiter: the delimiter to use
        collection  headers:   a collection of identifiers to use as headers
        encoding    encoding:  the encoding to use on the file"""
    assert type(rows) is list or type(
        rows) is tuple, "Rows arg must be a list/tuple of " \
        "either lists, tuples or dicts"
    assert len(rows) or headers, "Nothing to writeout"

    def write_dicts(headers):  # pass headers since we might modify it
        if not headers:
            headers = list(rows[0].keys())
        with open(outfile, 'w', encoding=encoding) as f:
            writer = csv.DictWriter(
                f, fieldnames=headers, delimiter=delimiter)
            writer.writeheader()
            writer.writerows(rows)

    def write_lists_or_tups():
        with open(outfile, 'w', encoding=encoding) as f:
            writer = csv.writer(f, delimiter=delimiter)
            writer.writerow(headers) if headers else None
            writer.writerows(rows)

    if rows:
        if type(rows[0]) is dict:
            write_dicts(headers)
        else:
            write_lists_or_tups()
    else:
        write_lists_or_tups()


def read_csv(infile, delimiter=',', encoding='utf-8', named=False):
    """Reads a csv as a list of lists (unnamed) or a list of named tuples (named)
    Args:
        string   infile:    the file to read in

        OPTIONAL:
        string   delimiter: the delimiter used (default ',')
        encoding encoding:  the encoding of the file (default 'utf-8')
        boolean  named:     if true, loads rows as named tuples
                            (default lists), (default False)

    Returns list of lists or named tuples"""
    with open(infile, encoding=encoding) as f:
        reader = csv.reader(f, delimiter=delimiter)
        if named:
            headers = next(reader)
            # strip spaces and annoying things from headers
            names = [identifier.replace('-', '_').replace(' ', '_').lower()
                     for identifier in headers]
            Data = namedtuple("Data", names)
            named_rows = map(Data._make, reader)
            return [row for row in named_rows]
        else:
            return list(list(row for row in reader))
