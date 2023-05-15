import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import URLError, HTTPError


class http_client:
    def __init__(self) -> None:
        pass

    def get(self, url, params=None, headers={}):
        if params:
            url += params
        request = Request(url, headers=headers, method="GET")
        try:
            with urlopen(request) as response:
                json_data = http_client.response2json(response)
                return json_data, response.getcode()
        except HTTPError as e:
            print("Error code: ", e.code)
            raise e
        except URLError as e:
            print("We failed to reach a server.")
            print("Reason: ", e.reason)
            raise e

    def post(self, url, data, params=None, headers={}):
        if params:
            url += params
        json_data = json.dumps(data).encode("utf-8")
        request = Request(url=url, data=json_data, method="POST", headers=headers)
        try:
            with urlopen(request) as response:
                json_data = http_client.response2json(response)
                return json_data, response.getcode()
        except HTTPError as e:
            print("HTTP Error: {}".format(e.reason))
            print("Error code: ", e.code)
            raise e
        except URLError as e:
            print("We failed to reach a server.")
            print("Reason: ", e.reason)
            raise e

    def put(self, url, data, params=None, headers={}):
        if params:
            url += params
        json_data = json.dumps(data).encode("utf-8")
        request = Request(url=url, data=json_data, method="PUT", headers=headers)
        try:
            with urlopen(request) as response:
                # return response empty?!
                json_data = http_client.response2json(response)
                return json_data, response.getcode()
        except HTTPError as e:
            print("HTTP Error: {}".format(e.reason))
            print("Error code: ", e.code)
            raise e
        except URLError as e:
            print("We failed to reach a server.")
            print("Reason: ", e.reason)
            raise e

    def delete(self, url, params=None, headers={}):
        if params:
            url += params
        request = Request(url=url, method="DELETE", headers=headers)
        try:
            with urlopen(request) as response:
                json_data = http_client.response2json(response)
                return json_data, response.getcode()
        except HTTPError as e:
            print("HTTP Error: {}".format(e.reason))
            print("Error code: ", e.code)
            raise e
        except URLError as e:
            print("We failed to reach a server.")
            print("Reason: ", e.reason)
            raise e

    def response2json(response_body):
        content = response_body.read().decode("utf-8")
        json_data = json.loads(content)
        return json_data
