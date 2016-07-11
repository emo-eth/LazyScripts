import json


class jwcache(object):

    cache_updated = False
    cache = {}

    def load_cache(self, name, destroy_on_fail=False):
        cache_temp = {}
        try:
            with open(name) as data_file:
                cache_temp = json.load(data_file)
                print('Cache loaded successfully.')
                return cache_temp
        except FileNotFoundError:
            print("Creating cache.")
            with open(name, 'w', encoding='utf-16') as outfile:
                json.dump(cache_temp, outfile)
            return cache_temp
        except Exception as e:
            print(type(e), e)
            if destroy_on_fail:
                print("Loading cache failed. Overwriting corrupt cache.")
                with open(name, 'w', encoding='utf-16') as outfile:
                    json.dump(cache_temp, outfile)
                return cache_temp
            else:
                raise e

    def write_cache(self, name, cache):
        if self.cache_updated:
            with open(name, 'w', encoding='utf-16') as outfile:
                json.dump(cache, outfile)


def load_cache(name, destroy_on_fail=False):
    cache_temp = {}
    try:
        with open(name) as data_file:
            cache_temp = json.load(data_file)
            print('Cache loaded successfully.')
            return cache_temp
    except FileNotFoundError:
        print("Creating cache.")
        with open(name, 'w', encoding='utf-16') as outfile:
            json.dump(cache_temp, outfile)
        return cache_temp
    except Exception as e:
        print(type(e), e)
        if destroy_on_fail:
            print("Loading cache failed. Overwriting corrupt cache.")
            with open(name, 'w', encoding='utf-16') as outfile:
                json.dump(cache_temp, outfile)
            return cache_temp
        else:
            raise e


def write_cache(name, cache):
    with open(name, 'w') as outfile:
        json.dump(cache, outfile)
