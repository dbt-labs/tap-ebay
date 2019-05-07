#!/usr/bin/env python3

import singer

import tap_framework

from tap_ebay.client import EbayClient
from tap_ebay.streams import AVAILABLE_STREAMS

LOGGER = singer.get_logger()  # noqa

CONFIG_KEYS = [
    "client_id",
    "client_secret",
    "refresh_token",
    "scope",
    "start_date"
]


class EbayRunner(tap_framework.Runner):
    pass


@singer.utils.handle_top_exception(LOGGER)
def main():
    args = singer.utils.parse_args(required_config_keys=CONFIG_KEYS)
    client = EbayClient(args.config)
    runner = EbayRunner(
        args, client, AVAILABLE_STREAMS)

    client.authorize()

    if args.discover:
        runner.do_discover()
    else:
        runner.do_sync()


if __name__ == '__main__':
    main()
