import csv


class jwcsv(object):

    def write_csv(self, outfile, rows, dict_headers=[], headers=[], encoding='utf-8'):
        '''Basis for writing out csv in a subclass'''
        if '.csv' in outfile:
            outfile = outfile.split('.csv')[0]
        if dict_headers:
            with open('%s.csv' % outfile, 'w', encoding=encoding) as outfile:
                writer = csv.DictWriter(outfile, dict_headers)
                writer.writeheader()
                writer.writerows(rows)
        else:
            with open('%s.csv' % outfile, 'w', encoding=encoding) as outfile:
                writer = csv.writer(outfile)
                writer.writerows(headers) if headers else None
                writer.writerows(rows)

    def read_csv(self, infile, encoding='utf-8'):
        reader = csv.reader(open(infile, encoding=encoding), delimiter=',')
        return list(list(row for row in reader))


def write_csv(outfile, rows, dict_headers=[], headers=[], encoding='utf-8'):
    if '.csv' in outfile:
        outfile = outfile.split('.csv')[0]
    if dict_headers:
        with open('%s.csv' % outfile, 'w', encoding=encoding) as outfile:
            writer = csv.DictWriter(outfile, dict_headers)
            writer.writeheader()
            writer.writerows(rows)
    else:
        with open('%s.csv' % outfile, 'w', encoding=encoding) as outfile:
            writer = csv.writer(outfile)
            writer.writerow(headers) if headers else None
            writer.writerows(rows)


def read_csv(infile, encoding='utf-8'):
    reader = csv.reader(open(infile, encoding=encoding), delimiter=',')
    return list(list(row for row in reader))
