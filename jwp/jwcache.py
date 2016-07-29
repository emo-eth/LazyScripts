import json


class jwcache(object):

    cache_updated = False
    cache = {}

    def load_cache(self, path, destroy_on_fail=False):
        assert type(path) is str, 'path must be string'
        cache_temp = {}
        try:
            with open(path) as data_file:
                cache_temp = json.load(data_file)
                print('Cache loaded successfully.')
                return cache_temp
        except FileNotFoundError:
            print("Creating cache.")
            with open(path, 'w', encoding='utf-16') as outfile:
                json.dump(cache_temp, outfile)
            return cache_temp
        except Exception as e:
            if destroy_on_fail:
                print(type(e), e)
                print("Loading cache failed. Overwriting corrupt cache.")
                with open(path, 'w', encoding='utf-16') as outfile:
                    json.dump(cache_temp, outfile)
                return cache_temp
            else:
                raise e

    def write_cache(self, path, cache):
        assert type(path) is str, 'path must be string'
        if self.cache_updated:
            with open(path, 'w', encoding='utf-16') as outfile:
                json.dump(cache, outfile)


def load_cache(path, destroy_on_fail=False):
    assert type(path) is str, 'path must be string'
    cache_temp = {}
    try:
        with open(path) as data_file:
            cache_temp = json.load(data_file)
            print('Cache loaded successfully.')
            return cache_temp
    except FileNotFoundError:
        print("Creating cache.")
        with open(path, 'w', encoding='utf-16') as outfile:
            json.dump(cache_temp, outfile)
        return cache_temp
    except Exception as e:
        if destroy_on_fail:
            print(type(e), e)
            print("Loading cache failed. Overwriting corrupt cache.")
            with open(path, 'w', encoding='utf-16') as outfile:
                json.dump(cache_temp, outfile)
            return cache_temp
        else:
            raise e


def write_cache(path, cache):
    assert type(path) is str, 'path must be string'
    with open(path, 'w') as outfile:
        json.dump(cache, outfile)
