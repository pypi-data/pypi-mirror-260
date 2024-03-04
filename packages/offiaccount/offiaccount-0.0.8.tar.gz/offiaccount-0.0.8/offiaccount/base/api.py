import httpx, json

class BaseAPI:
    def __init__(self, proxy=None):
        self.client = httpx.Client(proxy=proxy)

    def json_load(self, file, mode='r', encoding='utf-8', **kwargs):
        with open(file, mode=mode, encoding=encoding, **kwargs) as f:
            data = json.load(f)
        return data

    def json_dump(self, data, file, mode='w+', encoding='utf-8', indent=4, **kwargs):
        with open(file, mode=mode, encoding=encoding) as f:
            json.dump(data, f, ensure_ascii=False, indent=indent, **kwargs)
