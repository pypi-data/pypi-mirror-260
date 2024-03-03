import requests


class Http:
    def __init__(self):
        self.base_url = "https://rest.pubq.io"
        self.client = requests.Session()
        self.client.headers.update({"Content-Type": "application/json"})
        self.client.headers.update({"Accept": "application/json"})
        self.client.headers.update({"User-Agent": "PubqPython/1.2.0"})

    def request(self, method, endpoint, **kwargs):
        url = self.base_url + endpoint
        return self.client.request(method, url, **kwargs)

    def get(self, endpoint, **kwargs):
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self.request("PUT", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.request("DELETE", endpoint, **kwargs)

    def getClient(self):
        return self
