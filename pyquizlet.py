import random
from urllib.parse import urlencode, urljoin

import requests


class Quizlet():
  auth_url = 'https://quizlet.com/authorize'
  token_url = 'https://api.quizlet.com/oauth/token'
  api_url = 'https://api.quizlet.com/2.0'

  def __init__(self, client_id, encoded_auth_str):
    self.client_id = client_id
    self.encoded_auth_str = encoded_auth_str
    self.access_info = None

  def generate_auth_url(self, scope):
    state = '%010x' % random.randrange(16**10)
    params = {'scope': scope,
              'client_id': self.client_id,
              'response_type': 'code',
              'state': state}
    request_string = '?'. join([Quizlet.auth_url, urlencode(params)])
    return (request_string, state)

  def request_token(self, code, redirect_uri):
    params = {'grant_type': 'authorization_code',
              'code': code,
              'redirect_uri': redirect_uri}
    headers = {'Content-type': 'application/x-www-form-urlencoded',
               'Authorization' : 'Basic %s' % self.encoded_auth_str}
    r = requests.post(Quizlet.token_url, headers=headers, data=params)
    self.access_info = r.json()

  def make_request(self, api_path, params={}):
    base_url = '/'.join([Quizlet.api_url, api_path])
    print(base_url)
    params['client_id'] = self.client_id
    headers = {'Authorization': 'Bearer ' + self.access_info['access_token']}
    r = requests.get(base_url, headers=headers, params=params)
    return r.json()

