import csv


class jwcsv(object):

    def write_csv(self, outfile, rows, delimiter=',', headers=[], encoding='utf-8'):
        '''Basis for writing out csv in a subclass'''
        if type(rows) is dict:
            if not headers:
                headers = list(rows.keys())
            with open(outfile, 'w', encoding=encoding) as outfile:
                writer = csv.DictWriter(outfile, headers)
                writer.writeheader()
                writer.writerows(rows)
        else:
            with open(outfile, 'w', encoding=encoding) as outfile:
                writer = csv.writer(outfile)
                writer.writerows(headers) if headers else None
                writer.writerows(rows)

    def read_csv(self, infile, delimiter=',', encoding='utf-8'):
        reader = csv.reader(open(infile, encoding=encoding), delimiter=delimiter)
        return list(list(row for row in reader))


def write_csv(outfile, rows, delimiter=',', headers=[], encoding='utf-8'):
    if type(rows) is dict:
        if not headers:
            headers = list(rows.keys())
        with open(outfile, 'w', encoding=encoding) as outfile:
            writer = csv.DictWriter(outfile, fieldnames=headers, delimiter=delimiter)
            writer.writeheader()
            writer.writerows(rows)
    else:
        with open(outfile, 'w', encoding=encoding) as outfile:
            writer = csv.writer(outfile, delimiter=delimiter)
            writer.writerow(headers) if headers else None
            writer.writerows(rows)


def read_csv(infile, delimiter=',', encoding='utf-8'):
    reader = csv.reader(open(infile, encoding=encoding), delimiter=delimiter)
    return list(list(row for row in reader))
