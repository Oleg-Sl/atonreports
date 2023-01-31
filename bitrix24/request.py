#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Wrapper over Bitrix24 cloud API"""
import json
import time
from requests import adapters, post, exceptions

from . import tokens

adapters.DEFAULT_RETRIES = 10


class Bitrix24:
    api_url = 'https://%s/rest/%s.json'
    oauth_url = 'https://oauth.bitrix.info/oauth/token/'
    timeout = 60

    def __init__(self):
        token_data = tokens.get_secrets_all()
        self.domain = token_data.get("domain", None)
        self.auth_token = token_data.get("auth_token", None)
        self.refresh_token = token_data.get("refresh_token", None)
        self.client_id = tokens.get_secret("client_id")
        self.client_secret = tokens.get_secret("client_secret")

    def refresh_tokens(self):
        """Refresh access tokens
        :return:
        """
        r = {}
        try:
            # Make call to oauth server
            r = post(
                self.oauth_url,
                params={'grant_type': 'refresh_token', 'client_id': self.client_id, 'client_secret': self.client_secret,
                        'refresh_token': self.refresh_token})
            result = json.loads(r.text)

            # Renew access tokens
            self.auth_token = result['access_token']
            self.refresh_token = result['refresh_token']
            self.expires_in = result['expires_in']
            tokens.update_secrets(self.auth_token, self.expires_in, self.refresh_token)
            return True
        except (ValueError, KeyError):
            result = dict(error='Error on decode oauth response [%s]' % r.text)
            return result

    def call(self, method, params):
        try:
            url = self.api_url % (self.domain, method)
            url += '?auth=' + self.auth_token
            headers = {
                'Content-Type': 'application/json',
            }
            r = post(url, data=json.dumps(params), headers=headers, timeout=self.timeout)
            result = json.loads(r.text)
        except ValueError:
            pass
            result = dict(error='Error on decode api response [%s]' % r.text)
        except exceptions.ReadTimeout:
            result = dict(error='Timeout waiting expired [%s sec]' % str(self.timeout))
        except exceptions.ConnectionError:
            result = dict(error='Max retries exceeded [' + str(adapters.DEFAULT_RETRIES) + ']')

        if 'error' in result and result['error'] in ('NO_AUTH_FOUND', 'expired_token'):
            result_update_token = self.refresh_tokens()
            if result_update_token is not True:
                return result
            result = self.call(method, params)
        elif 'error' in result and result['error'] in ['QUERY_LIMIT_EXCEEDED', ]:
            time.sleep(2)
            return self.call(method, params)

        return result

    def batch(self, params):
        if 'halt' not in params or 'cmd' not in params:
            return dict(error='Invalid batch structure')

        return self.call("batch", params)

    # def request_list(self, method, fields=None, filter={}, id_start=0):
    #     filter[">ID"] = id_start
    #     params = {
    #         "order": {"ID": "ASC"},
    #         "filter": filter,
    #         "select": fields,
    #         "start": -1
    #     }
    #     data = self.request(method, params).get("result")
    #     if data and isinstance(data, dict) and "tasks" in data:
    #         data = data.get("tasks")
    #     if data and isinstance(data, list):
    #         id_start = data[-1].get("ID") or data[-1].get("id")
    #         data.extend(self.request_list(method, fields, filter, id_start))
    #
    #     return data
