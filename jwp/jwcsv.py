import csv


class jwcsv(object):

    def write_csv(self, outfile, rows, dict_headers=[], headers=[], delimiter=',', encoding='utf-8'):
        '''Basis for writing out csv in a subclass'''
        if dict_headers:
            with open(outfile, 'w', encoding=encoding) as outfile:
                writer = csv.DictWriter(outfile, dict_headers)
                writer.writeheader()
                writer.writerows(rows)
        else:
            with open(outfile, 'w', encoding=encoding) as outfile:
                writer = csv.writer(outfile)
                writer.writerows(headers) if headers else None
                writer.writerows(rows)

    def read_csv(self, infile, encoding='utf-8', delimiter=','):
        reader = csv.reader(open(infile, encoding=encoding), delimiter=delimiter)
        return list(list(row for row in reader))


def write_csv(outfile, rows, dict_headers=[], headers=[], delimiter=',', encoding='utf-8'):
    if dict_headers:
        with open(outfile, 'w', encoding=encoding) as outfile:
            writer = csv.DictWriter(outfile, fieldnames=dict_headers, delimiter=delimiter)
            writer.writeheader()
            writer.writerows(rows)
    else:
        with open(outfile, 'w', encoding=encoding) as outfile:
            writer = csv.writer(outfile, delimiter=delimiter)
            writer.writerow(headers) if headers else None
            writer.writerows(rows)


def read_csv(infile, encoding='utf-8', delimiter=','):
    reader = csv.reader(open(infile, encoding=encoding), delimiter=delimiter)
    return list(list(row for row in reader))
