def jwprint(*args, **kwargs):
    ''' bypasses UnicodeEncodeErrors with a try/except block
        TODO: recursive escaping'''
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        tuple_temp_list = []
        temp_kw = {}
        for item in args:
            item = escape(item)
            tuple_temp_list.append(item)
        for k, v in kwargs.items():
            v = escape(v)
            temp_kw[k] = v

        print(*tuple(tuple_temp_list), **kwargs)


def escape(item):
    if type(item) is dict:
        item = {escape(k): escape(v) for k, v in item.items()}
    elif type(item) is tuple:
        item = tuple(escape(x) for x in item)
    elif type(item) is list:
        item = [escape(x) for x in item]
    elif type(item) is str:
            item = unicode(item, 'utf-8')
    return item


jwprint('beyoncé', end='e')
