import requests
import singer
import singer.metrics
import base64

LOGGER = singer.get_logger()  # noqa
AUTH_URL = "https://api.ebay.com/identity/v1/oauth2/token"


class EbayClient:

    MAX_TRIES = 5

    def __init__(self, config):
        self.config = config
        self.token = None

    def authorize(self):
        client = "{}:{}".format(self.config.get('client_id'),
                                self.config.get('client_secret'))
        auth = base64.b64encode(client.encode()).decode()

        data = {
            "grant_type": "refresh_token",
            "scope": self.config.get('scope'),
            "refresh_token": self.config.get('refresh_token')
        }

        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Authorization': "Basic {}".format(auth),
            'User-Agent': self.config.get('user_agent')
        }

        response = requests.request("POST",
                                    AUTH_URL,
                                    data=data,
                                    headers=headers)

        response.raise_for_status()
        data = response.json()

        self.token = data['access_token']

    def make_request(self, url, method, params=None, body=None, attempt=0):
        LOGGER.info("Making {} request to {} ({})".format(method, url, params))

        response = requests.request(
            method,
            url,
            headers={
                'Authorization': "Bearer {}".format(self.token),
                'Content-Type': 'application/json',
                'User-Agent': self.config.get('user_agent')
            },
            params=params,
            data=body)

        LOGGER.info("Got response: {}".format(response.status_code))

        if response.status_code != 200:
            raise RuntimeError(response.text)

        return response.json()
