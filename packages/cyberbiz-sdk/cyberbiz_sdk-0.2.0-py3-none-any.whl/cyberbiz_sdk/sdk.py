import time
import hmac
import hashlib
import base64
import requests


class CyberbizSdk:
    def __init__(
        self, username: str, secret: str, api_host: str = "https://api.cyberbiz.co"
    ):
        self.username = username
        self.secret = secret.encode("utf-8")
        self.host = api_host

    def _get_date(self):
        return time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())

    def _get_signature(self, x_date: str, http_method: str, url_path: str) -> str:
        # request-line
        rline = f"{http_method} {url_path} HTTP/1.1"

        sig_str = f"x-date: {x_date}\n{rline}"

        return sig_str

    def _get_auth(self, sig_str: str):
        dig = hmac.new(
            self.secret, msg=sig_str.encode("utf-8"), digestmod=hashlib.sha256
        ).digest()
        sig = base64.b64encode(dig).decode()
        headers = "x-date request-line"
        auth = (
            'hmac username="'
            + self.username
            + '", algorithm="hmac-sha256", headers="'
            + headers
            + '", signature="'
            + sig
            + '"'
        )
        return auth

    def _get_headers(self, url_path: str, http_method: str = "GET"):
        x_date = self._get_date()
        sig = self._get_signature(
            x_date=x_date, http_method=http_method, url_path=url_path
        )
        auth = self._get_auth(sig)
        request_headers = {"X-Date": x_date, "Authorization": auth}
        return request_headers

    def get(self, url_path, params=None, page=1, per_page=5, offset=0):
        if params is None:
            params = {}

        params.update(
            {
                "page": page,
                "per_page": per_page,
                "offset": offset,
            }
        )
        # payload = f'page={page}&per_page={per_page}&offset={offset}'
        request_headers = self._get_headers(url_path)
        url = self.host + url_path

        r = requests.get(url, headers=request_headers, params=params)
        return r

    def _post(self, url_path, data=None):
        if data is None:
            data = {}

        request_headers = self._get_headers(url_path, http_method="POST")
        url = self.host + url_path

        r = requests.post(url, headers=request_headers, json=data)
        return r

    def get_products(self, page=1, per_page=50, offset=0):
        url_path = "/v1/products"

        return self.get(url_path, None, page, per_page, offset)

    def get_customers(self, page=1, per_page=50, offset=0):
        url_path = "/v1/customers"
        return self.get(url_path, None, page, per_page, offset)

    def get_customer_by_id(self, customer_id):
        url_path = f"/v1/customers/{customer_id}"
        return self.get(url_path)

    def get_customers_by(
        self, emails=None, mobiles=None, page=1, per_page=50, offset=0
    ):
        url_path = "/v1/customers/get_customer_id"
        search_params = {}
        if emails:
            emails_str = ",".join(emails)
            search_params.update({"customer_emails": emails_str})
        if mobiles:
            mobiles_str = ",".join(mobiles)
            search_params.update({"customer_mobiles": mobiles_str})

        return self.get(url_path, search_params, page, per_page, offset)

    def get_customer_coupons(self, customer_id, page=1, per_page=50, offset=0):
        url_path = f"/v1/customers/{customer_id}/coupons"
        return self.get(url_path, None, page, per_page, offset)

    def get_customer_coupon_by_id(self, customer_id, coupon_id):
        url_path = f"/v1/customers/{customer_id}/coupons/{coupon_id}"
        return self.get(url_path)

    def create_coupon_to_customer(self, customer_id, payload):
        url_path = f"/v1/customers/{customer_id}/coupons"
        return self._post(url_path, payload)
