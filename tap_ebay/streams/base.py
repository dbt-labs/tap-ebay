import singer
import singer.utils
import singer.metrics

from dateutil.parser import parse
from tap_ebay.config import get_config_start_date
from tap_ebay.state import incorporate, save_state, \
    get_last_record_value_for_table

from tap_framework.streams import BaseStream as base


LOGGER = singer.get_logger()


class BaseStream(base):
    KEY_PROPERTIES = ['id']

    def get_url(self):
        return 'https://api.ebay.com{}'.format(self.path)

    def get_schema(self):
        schema = self.load_schema_by_name(self.TABLE)
        return singer.resolve_schema_references(schema, None)

    def get_filter(self, start_date):
        return 'lastmodifieddate:[{}..]'.format(start_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))

    def get_params(self, start_date, offset, limit):
        return {
            'filter': self.get_filter(start_date),
            'limit': limit,
            'offset': offset
        }

    def sync_data(self):
        table = self.TABLE

        date = get_last_record_value_for_table(self.state, table)

        if date is None:
            date = get_config_start_date(self.config)

        LOGGER.info('Syncing data from {}'.format(date.isoformat()))
        url = self.get_url()

        offset = 0
        limit = 100
        page = 0

        while True:
            LOGGER.info("Syncing page {} for stream {}".format(page, table))
            params = self.get_params(date, offset, limit)
            result = self.client.make_request(url, self.API_METHOD,
                                              params=params)

            data = self.get_stream_data(result)

            with singer.metrics.record_counter(endpoint=table) as counter:
                singer.write_records(table, data)
                counter.increment(len(data))

            if len(data) > 0:
                last_record = data[-1]
                last_record_date = last_record['lastModifiedDate']

                self.state = incorporate(self.state,
                                         table,
                                         'last_record',
                                         last_record_date)

            save_state(self.state)

            page += 1
            offset += limit
            if offset > result['total']:
                break

        return self.state

    def get_stream_data(self, result):
        return [
            self.transform_record(record)
            for record in result
        ]
