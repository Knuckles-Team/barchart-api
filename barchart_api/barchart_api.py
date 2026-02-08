#!/usr/bin/python
# coding: utf-8

import sys
import re
from typing import Dict, Any, Optional

import requests
import urllib3
from pydantic import ValidationError

from barchart_api.barchart_models import (
    GetStockModel,
    GetTopOwnModel,
    HistoricalItem,
    TopOwnItem,
    Response,
)
from barchart_api.decorators import require_auth
from barchart_api.exceptions import (
    AuthError,
    UnauthorizedError,
    ParameterError,
    MissingParameterError,
)


class Api(object):

    def __init__(
            self,
            url: str = "https://www.barchart.com/",
            proxies: Optional[dict] = None,
            verify: Optional[bool] = True,
    ):
        self._session = requests.Session()
        self.url = url.rstrip("/")
        self.headers = None
        self.verify = verify
        self.proxies = proxies

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
            print(
                f"Error: {e}\n"
                f"Unable to parse cookie_headers as JSON"
                f"Headers: {cookie_response}\n"
            )
            sys.exit(2)

        cookie = cookie_headers["Set-Cookie"]
        xsrf_token = re.findall("XSRF-TOKEN=[A-Za-z0-9]*", cookie_headers["Set-Cookie"])
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

    ####################################################################################################################
    #                                                  Stock API                                                       #
    ####################################################################################################################
    @require_auth
    def get_stock(self, **kwargs) -> Response:
        """
        Get historical stock data for a symbol.

        :param symbol: The stock symbol.
        :type symbol: str
        :param data: Data frequency (e.g., 'daily').
        :type data: str
        :param volume: Volume type (e.g., 'contract').
        :type volume: str
        :param order: Sort order (e.g., 'asc').
        :type order: str
        :param dividends: Include dividends.
        :type dividends: bool
        :param backadjust: Back-adjust for splits.
        :type backadjust: bool
        :param daystoexpiration: Days to expiration.
        :type daystoexpiration: int
        :param contractroll: Contract roll method (e.g., 'expiration').
        :type contractroll: str
        :param max_records: Maximum records to return.
        :type max_records: int

        :return: Response containing list of parsed Pydantic models with historical data.
        :rtype: Response

        :raises MissingParameterError: If symbol is not provided.
        :raises ParameterError: If parameters are invalid.
        """
        try:
            model = GetStockModel(**kwargs)
            response = self._session.get(
                url=f"{self.url}/proxies/timeseries/queryeod.ashx",
                params=model.api_parameters,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()  # Raise if HTTP error
            # Parse CSV (assuming format: symbol,timestamp,open,high,low,close,volume,openInterest)
            lines = response.text.strip().split('\n')
            parsed_data = []
            for line in lines:
                if line:
                    parts = line.split(',')
                    if len(parts) >= 7:
                        item_dict = {
                            'symbol': parts[0],
                            'timestamp': parts[1],
                            'open': float(parts[2]),
                            'high': float(parts[3]),
                            'low': float(parts[4]),
                            'close': float(parts[5]),
                            'volume': int(parts[6]),
                        }
                        if len(parts) > 7:
                            item_dict['openInterest'] = int(parts[7])
                        parsed_data.append(HistoricalItem.model_validate(item_dict))
            return Response(response=response, result=parsed_data)
        except ValidationError as ve:
            print(f"Invalid parameters or response data: {ve.errors()}")
            raise
        except Exception as e:
            print(f"Error during API call: {e}")
            raise

    ####################################################################################################################
    #                                                  Top Own API                                                     #
    ####################################################################################################################
    @require_auth
    def get_top_stocks_top_own(self, **kwargs) -> Response:
        """
        Get top stocks based on ownership signals.

        :param order_dir: Sort direction (e.g., 'asc').
        :type order_dir: str
        :param order_by: Field to sort by (e.g., 'symbol').
        :type order_by: str
        :param meta: Meta fields.
        :type meta: str
        :param fields: Fields to include.
        :type fields: str
        :param has_options: Filter for options availability.
        :type has_options: bool
        :param max_pages: Maximum pages to fetch (capped at 3).
        :type max_pages: int
        :param per_page: Records per page.
        :type per_page: int

        :return: Response containing list of parsed Pydantic models with top stocks data.
        :rtype: Response

        :raises ParameterError: If parameters are invalid.
        """
        try:
            model = GetTopOwnModel(**kwargs)
            all_parsed = []
            max_pages = model.max_pages if model.max_pages <= 3 else 3
            last_response = None
            base_url = f"{self.url}/proxies/core-api/v1/quotes/get"
            for page in range(max_pages):
                params = model.api_parameters.copy()
                params['lists'] = 'stocks.us.signals_ratings.v2_top'
                params['limit'] = model.per_page
                params['page'] = page
                params['raw'] = 1
                response = self._session.get(
                    url=base_url,
                    params=params,
                    headers=self.headers,
                    verify=self.verify,
                    proxies=self.proxies,
                )
                response.raise_for_status()  # Raise if HTTP error
                json_response = response.json()
                result_data = json_response.get('data', json_response)
                parsed_page = [TopOwnItem.model_validate(item) for item in result_data]
                all_parsed.extend(parsed_page)
                last_response = response
            return Response(response=last_response, result=all_parsed)
        except ValidationError as ve:
            print(f"Invalid parameters or response data: {ve.errors()}")
            raise
        except Exception as e:
            print(f"Error during API call: {e}")
            raise

    @require_auth
    def get_top_etfs_top_own(self, **kwargs) -> Response:
        """
        Get top ETFs based on ownership signals.

        :param order_dir: Sort direction (e.g., 'asc').
        :type order_dir: str
        :param order_by: Field to sort by (e.g., 'symbol').
        :type order_by: str
        :param meta: Meta fields.
        :type meta: str
        :param fields: Fields to include.
        :type fields: str
        :param has_options: Filter for options availability.
        :type has_options: bool
        :param max_pages: Maximum pages to fetch (capped at 3).
        :type max_pages: int
        :param per_page: Records per page.
        :type per_page: int

        :return: Response containing list of parsed Pydantic models with top ETFs data.
        :rtype: Response

        :raises ParameterError: If parameters are invalid.
        """
        try:
            model = GetTopOwnModel(**kwargs)
            all_parsed = []
            max_pages = model.max_pages if model.max_pages <= 3 else 3
            last_response = None
            base_url = f"{self.url}/proxies/core-api/v1/quotes/get"
            for page in range(max_pages):
                params = model.api_parameters.copy()
                params['lists'] = 'etfs.us.signals_ratings.v2_top'
                params['limit'] = model.per_page
                params['page'] = page
                params['raw'] = 1
                response = self._session.get(
                    url=base_url,
                    params=params,
                    headers=self.headers,
                    verify=self.verify,
                    proxies=self.proxies,
                )
                response.raise_for_status()  # Raise if HTTP error
                json_response = response.json()
                result_data = json_response.get('data', json_response)
                parsed_page = [TopOwnItem.model_validate(item) for item in result_data]
                all_parsed.extend(parsed_page)
                last_response = response
            return Response(response=last_response, result=all_parsed)
        except ValidationError as ve:
            print(f"Invalid parameters or response data: {ve.errors()}")
            raise
        except Exception as e:
            print(f"Error during API call: {e}")
            raise