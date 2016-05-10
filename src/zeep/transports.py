import requests

from zeep.cache import SqliteCache


class Transport(object):

    def __init__(self, cache=None, timeout=300, verify=True, **kwargs):
        self.cache = cache or SqliteCache()
        self.timeout = timeout
        self.verify = verify
        self.request_args = kwargs

    def load(self, url):
        if self.cache:
            response = self.cache.get(url)
            if response:
                return bytes(response)

        response = requests.get(url, timeout=self.timeout, verify=self.verify, **self.request_args)

        if self.cache:
            self.cache.add(url, response.content)

        return response.content

    def post(self, address, message, headers):
        response = requests.post(
            address, data=message, headers=headers, verify=self.verify, **self.request_args
        )
        return response
