# coding: utf-8
"""REST-style HTTP client wrapper over requests."""

from __future__ import annotations

__author__ = "Bartek Kryza"
__copyright__ = "Copyright (C) 2023 Onedata"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt")

import json
import logging
from typing import Any

from onedatafilerestclient import OnedataRESTError

import requests


class HttpClient:
    """REST-style wrapper over requests library."""
    timeout: int = 5
    session: requests.Session

    def __init__(self, *, verify_ssl: bool = True) -> None:
        """Construct OnedataFileClient instance."""
        self.session = requests.Session()
        self.session.verify = verify_ssl

    def get_session(self) -> requests.Session:
        """Return requests session instance."""
        return self.session

    def _send_request(self,
                      method: str,
                      url: str,
                      data: Any = None,
                      headers: dict[str, str] = {},
                      *,
                      stream: bool = False) -> requests.Response:
        """Perform an HTTP request."""
        if 'Content-type' not in headers:
            headers['Content-type'] = 'application/json'

        req = requests.Request(method, url, data=data, headers=headers)
        prepared = self.session.prepare_request(req)
        response = self.session.send(prepared,
                                     stream=stream,
                                     timeout=self.timeout)

        if not response.ok:
            logging.debug(f"ERROR: {method} {url} '{response.text}'")
            raise OnedataRESTError.from_response(response)

        return response

    def get(self,
            url: str,
            data: Any = None,
            headers: dict[str, str] = {},
            *,
            stream: bool = False) -> requests.Response:
        """Perform a GET request."""
        return self._send_request('GET', url, data, headers, stream=stream)

    def put(self,
            url: str,
            data: Any = None,
            headers: dict[str, str] = {}) -> requests.Response:
        """Perform a PUT request."""
        if isinstance(data, dict):
            body = json.dumps(data)
        else:
            body = data

        return self._send_request('PUT', url, body, headers)

    def post(self,
             url: str,
             data: Any = None,
             headers: dict[str, str] = {}) -> requests.Response:
        """Perform a POST request."""
        if isinstance(data, dict):
            body = json.dumps(data)
        else:
            body = data

        return self._send_request('POST', url, body, headers)

    def delete(self,
               url: str,
               data: Any = None,
               headers: dict[str, str] = {}) -> requests.Response:
        """Perform a DELETE request."""
        return self._send_request('DELETE', url, data, headers)

    def head(self,
             url: str,
             data: Any = None,
             headers: dict[str, str] = {}) -> requests.Response:
        """Perform a HEAD request."""
        return self._send_request('HEAD', url, data, headers)
