import csv


class jwcsv(object):

    def write_csv(self, outfile, rows, dict_headers=[], headers=[]):
        '''Basis for writing out csv in a subclass'''
        if '.csv' in outfile:
            outfile = outfile.split('.csv')[0]
        if dict_headers:
            with open('%s.csv' % outfile, 'w', encoding='utf-8') as outfile:
                writer = csv.DictWriter(outfile, dict_headers)
                writer.writerows(rows)
        else:
            with open('%s.csv' % outfile, 'w', encoding='utf-8') as outfile:
                writer = csv.writer(outfile, headers)
                writer.writerows(rows)

    def read_csv(self, infile):
        reader = csv.reader(open(infile, encoding='utf-8'), delimiter=',')
        return list(list(row for row in reader))


def write_csv(outfile, rows, dict_headers=[], headers=[]):
    if '.csv' in outfile:
        outfile = outfile.split('.csv')[0]
    if dict_headers:
        with open('%s.csv' % outfile, 'w', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, dict_headers)
            writer.writerows(rows)
    else:
        with open('%s.csv' % outfile, 'w', encoding='utf-8') as outfile:
            writer = csv.writer(outfile, headers)
            writer.writerows(rows)


def read_csv(infile):
    reader = csv.reader(open(infile, encoding='utf-8'), delimiter=',')
    return list(list(row for row in reader))
