#!/usr/bin/python
# coding: utf-8

import sys
import re
import json
import requests
import urllib3

try:
    from barchart_api.decorators import require_auth
except ModuleNotFoundError:
    from decorators import require_auth
try:
    from barchart_api.exceptions import (AuthError, UnauthorizedError, ParameterError, MissingParameterError)
except ModuleNotFoundError:
    from exceptions import (AuthError, UnauthorizedError, ParameterError, MissingParameterError)


class Api(object):

    def __init__(self, url: str = "https://www.barchart.com/", verify: bool = True):
        self._session = requests.Session()
        self.url = url.rstrip('/')
        self.headers = None
        self.verify = verify

        if self.verify is False:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        cookie_url = "https://www.barchart.com/stocks/signals/top-bottom/top?orderBy=symbol&orderDir=asc"

        cookie_request_headers = {
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        }
        cookie_response = requests.get(url=cookie_url, headers=cookie_request_headers)

        if cookie_response.status_code == 403:
            raise UnauthorizedError
        elif cookie_response.status_code == 401:
            raise AuthError
        elif cookie_response.status_code == 404:
            raise ParameterError

        try:
            cookie_headers = cookie_response.headers
        except Exception as e:
            print(f"Error: {e}\n"
                  f"Unable to parse cookie_headers as JSON"
                  f"Headers: {cookie_response}\n")
            sys.exit(2)

        cookie = cookie_headers['Set-Cookie']
        xsrf_token = re.findall("XSRF-TOKEN=[A-Za-z0-9]*", cookie_headers['Set-Cookie'])
        if xsrf_token and cookie:
            xsrf_token = re.sub("XSRF-TOKEN=", "", xsrf_token[0])
            self.headers = {
                "content-type": "application/json",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
                "cookie": cookie,
                "x-xsrf-token": xsrf_token,
            }
        else:
            raise MissingParameterError

    def get_stock(self, symbol: str = None,
                  fields: str = "&data=daily"
                                "&volume=contract"
                                "&order=asc"
                                "&dividends=false"
                                "&backadjust=false"
                                "&daystoexpiration=1"
                                "&contractroll=expiration",
                  max_records: int = 640):
        if not symbol:
            raise MissingParameterError
        api_filter = f"?symbol={symbol}"
        if fields:
            if not isinstance(fields, str):
                raise ParameterError
            api_filter = f'{api_filter}&fields={fields}'
        if max_records:
            if not isinstance(max_records, int):
                raise ParameterError
            api_filter = f'{api_filter}&maxrecords={max_records}'
        response = self._session.get(
            f'{self.url}/proxies/timeseries/queryeod.ashx{api_filter}', headers=self.headers, verify=self.verify)
        return response


    def get_top_stocks_top_own(self, ordering: str = "asc", order_by: str = "symbol",
                               meta: str = "field.shortName%2Cfield.type%2Cfield.description%2Clists.lastUpdate",
                               fields: str = "symbol%2CsymbolName%2ClastPrice%2CpriceChange%2CpercentChange%2Copinion%2CopinionPrevious%2CopinionLastWeek%2CopinionLastMonth%2CsymbolCode%2CsymbolType%2ChasOptions",
                               has_options: bool = True,
                               max_pages: int = 1,
                               per_page: int = 100):
        response = []
        api_filter = ""
        if ordering:
            if not isinstance(ordering, str):
                raise ParameterError
            api_filter = f'{api_filter}&orderDir={ordering}'
        if fields:
            if not isinstance(fields, str):
                raise ParameterError
            api_filter = f'{api_filter}&fields={fields}'
        if order_by:
            if not isinstance(order_by, str):
                raise ParameterError
            api_filter = f'{api_filter}&orderBy={order_by}'
        if meta:
            if not isinstance(meta, str):
                raise ParameterError
            api_filter = f'{api_filter}&meta={meta}'
        if has_options:
            if not isinstance(has_options, bool):
                raise ParameterError
            api_filter = f'{api_filter}&hasOptions={str(has_options).lower()}'
        if max_pages == 0 or max_pages > 3:
            max_pages = 3
        for page in range(0, max_pages):
            response_page = self._session.get(
                f'{self.url}/proxies/core-api/v1/quotes/get?lists=stocks.us.signals_ratings.v2_top{api_filter}&limit={per_page}&page={page}&raw=1',
                headers=self.headers, verify=self.verify)
            response.append(response_page)
        return response

    def get_top_etfs_top_own(self, ordering: str = "asc", order_by: str = "symbol",
                             meta: str = "field.shortName%2Cfield.type%2Cfield.description%2Clists.lastUpdate",
                             fields: str = "symbol%2CsymbolName%2ClastPrice%2CpriceChange%2CpercentChange%2Copinion%2CopinionPrevious%2CopinionLastWeek%2CopinionLastMonth%2CsymbolCode%2CsymbolType%2ChasOptions",
                             has_options: bool = True,
                             max_pages: int = 1,
                             per_page: int = 100):
        response = []
        api_filter = ""
        if ordering:
            if not isinstance(ordering, str):
                raise ParameterError
            api_filter = f'{api_filter}&orderDir={ordering}'
        if fields:
            if not isinstance(fields, str):
                raise ParameterError
            api_filter = f'{api_filter}&fields={fields}'
        if order_by:
            if not isinstance(order_by, str):
                raise ParameterError
            api_filter = f'{api_filter}&orderBy={order_by}'
        if meta:
            if not isinstance(meta, str):
                raise ParameterError
            api_filter = f'{api_filter}&meta={meta}'
        if has_options:
            if not isinstance(has_options, bool):
                raise ParameterError
            api_filter = f'{api_filter}&hasOptions={str(has_options).lower()}'
        if max_pages == 0 or max_pages > 3:
            max_pages = 3
        for page in range(0, max_pages):
            response_page = self._session.get(
                f'{self.url}/proxies/core-api/v1/quotes/get?lists=etfs.us.signals_ratings.v2_top{api_filter}&limit={per_page}&page={page}',
                headers=self.headers, verify=self.verify)
            response.append(response_page)
        return response


# if __name__ == "__main__":
#     barchart_client = Api(url="https://www.barchart.com/")
#     top_stocks_responses = barchart_client.get_top_stocks_top_own(max_pages=1)
#     top_stocks = []
#     for top_stocks_response in top_stocks_responses:
#         try:
#             top_stocks.append(top_stocks_response.json())
#         except Exception as e:
#             print(f"Top Stocks ERROR: {top_stocks_response}")
#     print(f"Top Stocks: {top_stocks}")
#     top_stocks = top_stocks[0]['data']
#     with open("data2.json", "w") as f:
#         json.dump({"stocks": top_stocks}, f, indent=4)
