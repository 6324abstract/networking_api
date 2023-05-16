from p1.src.client import http_client
import unittest
from urllib.error import URLError, HTTPError


class HttpRequestTest(unittest.TestCase):
    "Fixture that creates a api URL and client to use for making request"

    def setUp(self) -> None:
        self.baseurl = "https://dummyjson.com/products"
        self.test_client = http_client()
        self.headers = HttpRequestTest.correct_task_headers()

    def tearDown(self) -> None:
        pass

    def test_successsful_get_request(self):
        response, code = self.test_client.get(url=self.baseurl + "/1")
        assert code == 200
        assert response["id"] == 1
        assert response["title"] == "iPhone 9"

    def test_succssful_get_request_with_params(self):
        response, code = self.test_client.get(
            url=self.baseurl + "/1",
            params=HttpRequestTest.new_get_query(),
        )
        assert code == 200
        assert response["id"] == 1
        assert response["price"] == 549

    def test_failed_get_request_with_wrong_params(self):
        """test with param starts with '!' expect 404 not found"""
        with self.assertRaises(URLError):
            self.test_client.get(
                url=self.baseurl + "/1",
                params="!" + HttpRequestTest.new_get_query(),
            )

    def test_failed_get_request_with_wrong_url(self):
        """test with wrong url"""
        with self.assertRaises(URLError):
            self.test_client.get(
                url=self.baseurl + "/wrongurl",
            )

    # def test_failed_get_request_with_wrong_header(self):
    #     """test with wrong header,expect http error"""

    #     with self.assertRaises(HTTPError):
    #         response, code = self.test_client.get(
    #             url=self.baseurl, headers=HttpRequestTest.wrong_task_headers()
    #         )

    def test_failed_post_request_with_wrong_data(self):
        """test with illeage data form, expect http error"""
        with self.assertRaises(HTTPError):
            self.test_client.post(
                url=self.baseurl + "/add",
                data=HttpRequestTest.wrong_payload(),
                headers=self.headers,
            )

    def test_failed_post_request_with_wrong_url(self):
        """test with wrong url"""
        with self.assertRaises(URLError):
            self.test_client.post(
                url=self.baseurl + "/wrongurl",
                data=HttpRequestTest.post_payload(),
                headers=self.headers,
            )

    def test_post_request(self):
        response, code = self.test_client.post(
            url=self.baseurl + "/add",
            data=HttpRequestTest.post_payload(),
            headers=self.headers,
        )
        assert code == 200
        assert response["id"] == 101
        assert response["title"] == "BMW Pencil"

    def test_failed_put_request_with_wrong_data(self):
        """test with illeage data form, expect http error"""
        with self.assertRaises(HTTPError):
            self.test_client.put(
                url=self.baseurl + "/1",
                data=HttpRequestTest.wrong_payload(),
                headers=self.headers,
            )

    def test_failed_put_request_with_wrong_url(self):
        """test with wrong url"""
        with self.assertRaises(URLError):
            self.test_client.put(
                url=self.baseurl + "/wrongurl",
                data=HttpRequestTest.put_payload(),
                headers=self.headers,
            )

    def test_put_request(self):
        response, code = self.test_client.put(
            url=self.baseurl + "/1",
            data=HttpRequestTest.put_payload(),
            headers=self.headers,
        )
        assert code == 200
        assert response["id"] == 1
        assert response["title"] == HttpRequestTest.put_payload()["title"]

    def test_failed_deleted_request_with_wrong_id(self):
        with self.assertRaises(HTTPError):
            self.test_client.delete(
                url=self.baseurl + "/-1",
                headers=self.headers,
            )

    def test_delete_request(self):
        response, code = self.test_client.delete(
            url=self.baseurl + "/1", headers=self.headers
        )

        assert code == 200
        assert response["isDeleted"] == True

    def post_payload():
        return {"title": "BMW Pencil"}

    def put_payload():
        return {"title": "iPhone Galaxy +1"}

    def correct_task_headers():
        return {"Content-Type": "application/json"}

    def wrong_task_headers():
        return {"Content-Type": "application/jon"}

    def wrong_payload():
        return "iphone"

    def new_get_query():
        return "?limit=10&skip=10&select=title,price"


if __name__ == "__main__":
    unittest.main()
