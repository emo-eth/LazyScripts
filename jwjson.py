import json


def load_json(path, encoding='utf-16', destroy_on_fail=False,
              touch=False, verbose=False):
    assert type(path) is str, 'path must be string'
    cache_temp = {}
    try:
        with open(path, 'r', encoding=encoding) as data_file:
            cache_temp = json.load(data_file)
            print('Json loaded successfully.') if verbose else None
            return cache_temp
    except FileNotFoundError as e:
        if touch:
            print("Creating json.") if verbose else None
            with open(path, 'w', encoding=encoding) as outfile:
                json.dump(cache_temp, outfile)
            return cache_temp
        else:
            raise e
    except Exception as e:
        if destroy_on_fail:
            print(type(e), e)
            print("Loading cache failed. Overwriting corrupt cache.")
            with open(path, 'w', encoding=encoding) as outfile:
                json.dump(cache_temp, outfile)
            return cache_temp
        else:
            raise e


def write_json(path, out, encoding='utf-16'):
    assert type(path) is str, 'path must be string'
    with open(path, 'w', encoding=encoding) as outfile:
        json.dump(out, outfile)

# alternate names
read_json = load_json

# deprecated api, for backwards-compatibility
load_cache = load_json
read_cache = load_json
write_cache = write_json

# deprecated super-class


class jwjson(object):

    cache_updated = False
    cache = {}

    def load_json(self, path, encoding='utf-16', destroy_on_fail=False,
                  touch=False, verbose=False):
        assert type(path) is str, 'path must be string'
        cache_temp = {}
        try:
            with open(path) as data_file:
                cache_temp = json.load(data_file)
                print('Json loaded successfully.') if verbose else None
                return cache_temp
        except FileNotFoundError as e:
            if touch:
                print("Creating json.") if verbose else None
                with open(path, 'w', encoding=encoding) as outfile:
                    json.dump(cache_temp, outfile)
                return cache_temp
            else:
                raise e
        except Exception as e:
            if destroy_on_fail:
                print(type(e), e)
                print("Loading cache failed. Overwriting corrupt cache.")
                with open(path, 'w', encoding=encoding) as outfile:
                    json.dump(cache_temp, outfile)
                return cache_temp
            else:
                raise e

    def write_json(self, path, out, encoding='utf-16'):
        assert type(path) is str, 'path must be string'
        if self.cache_updated:
            with open(path, 'w', encoding=encoding) as outfile:
                json.dump(out, outfile)

    read_json = load_json
    load_cache = load_json
    read_cache = load_json
    write_cache = write_json

jwcache = jwjson
