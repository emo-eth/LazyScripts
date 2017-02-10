#!/usr/bin/env python

import csv
from itertools import chain
from collections import namedtuple, Iterable


def write_csv(outfile, rows, delimiter=',', headers=[], encoding='utf-8'):
    """Creates a csv file with a given name from the given rows
    TODO: Add support for writing out namedtuples with headers
    Args:
        string     outfile:    the file to writeout
        iterable   rows:       a collection of rows, each a collection
                               (eg, a list of lists)

        OPTIONAL:
        string      delimiter: the delimiter to use
        collection  headers:   a collection of identifiers to use as headers
        encoding    encoding:  the encoding to use on the file"""
    assert isinstance(rows, Iterable), "Rows arg must be iterable"

    def write_dicts(headers):  # pass headers since we might modify it
        if not headers:
            headers = list(first_elem.keys())
        with open(outfile, 'w', encoding=encoding) as f:
            writer = csv.DictWriter(
                f, fieldnames=headers, delimiter=delimiter)
            writer.writeheader()
            writer.writerows(rows)

    def write_rows(headers):
        if isinstance(first_elem, tuple):
            try:
                headers = first_elem._fields
            except AttributeError:
                pass
        with open(outfile, 'w', encoding=encoding) as f:
            writer = csv.writer(f, delimiter=delimiter)
            writer.writerow(headers) if headers else None
            writer.writerows(rows)

    def _get_next(rows):
        try:
            return next(rows), rows
        except TypeError:
            temp = rows[0]
            rows = rows[1:]
            # update rows and return it since slicing will only
            # modify it in this namespace
            return temp, rows

    # get first element to decide if we're writing dicts
    first_elem, rows = _get_next(rows)
    # chain first and rest together
    rows = chain([first_elem], rows)
    if isinstance(first_elem, dict):
        write_dicts(headers)
    else:
        write_rows(headers)


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
