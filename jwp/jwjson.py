import json


class jwcache(object):

    cache_updated = False
    cache = {}

    def load_json(self, path, encoding='utf-16', destroy_on_fail=False):
        assert type(path) is str, 'path must be string'
        cache_temp = {}
        try:
            with open(path) as data_file:
                cache_temp = json.load(data_file)
                print('Cache loaded successfully.')
                return cache_temp
        except FileNotFoundError:
            print("Creating cache.")
            with open(path, 'w', encoding=encoding) as outfile:
                json.dump(cache_temp, outfile)
            return cache_temp
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

    def load_cache(self, path, encoding='utf-16', destroy_on_fail=False):
        self.load_json(path, encoding, destroy_on_fail)

    def write_cache(self, path, out, encoding='utf-16'):
        self.write_json(path, out, encoding)


def load_json(path, encoding='utf-16', destroy_on_fail=False):
    assert type(path) is str, 'path must be string'
    cache_temp = {}
    try:
        with open(path) as data_file:
            cache_temp = json.load(data_file)
            print('Cache loaded successfully.')
            return cache_temp
    except FileNotFoundError:
        print("Creating cache.")
        with open(path, 'w', encoding=encoding) as outfile:
            json.dump(cache_temp, outfile)
        return cache_temp
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


# deprecated api, for backwards-compatibility
def load_cache(path, encoding='utf-16', destroy_on_fail=False):
    load_json(path, encoding, destroy_on_fail)


def write_cache(path, out, encoding='utf-16'):
    write_json(path, out, encoding)
