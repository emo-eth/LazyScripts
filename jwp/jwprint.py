def jwprint(*args):
    ''' bypasses UnicodeEncodeErrors with a try/except block '''
    try:
        print(*args)
    except UnicodeEncodeError:
        tuple_temp_list = []
        for item in args:
            if type(item) is dict:
                item = {k.encode('utf-8'): v.encode('utf8') for k, v in item.items()}
            elif type(item) is list:
                print('list')
                item = [x.encode('utf-8') for x in item]
            elif type(item) is tuple:
                item = tuple(x.encode('utf-8') for x in item)
            elif type(item) is str:
                item = item.encode('utf-8')
            else:
                print('unhandled type:', type(item))
            tuple_temp_list.append(item)
        print(*tuple(tuple_temp_list))
