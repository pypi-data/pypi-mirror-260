import unittest
from parameterized import parameterized
from iqrfpy.enums.commands import OSResponseCommands
from iqrfpy.enums.message_types import OSMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.peripherals.os.responses.test_rf_signal import TestRfSignalResponse
from tests.helpers.json import generate_json_response
from iqrfpy.response_factory import ResponseFactory

data_ok: dict = {
    'mtype': OSMessages.TEST_RF_SIGNAL,
    'msgid': 'testRfSignalTest',
    'nadr': 0,
    'hwpid': 0,
    'rcode': 0,
    'dpa_value': 90,
    'result': {
        'counter': 3
    },
    'dpa': b'\x00\x00\x02\x8c\x00\x00\x00\x5a\x03'
}

data_ok_1: dict = {
    'mtype': OSMessages.TEST_RF_SIGNAL,
    'msgid': 'testRfSignalTest',
    'nadr': 0,
    'hwpid': 1026,
    'rcode': 0,
    'dpa_value': 35,
    'result': {
        'counter': 0
    },
    'dpa': b'\x00\x00\x02\x8c\x02\x04\x00\x23\x00'
}

data_ok_2: dict = {
    'mtype': OSMessages.TEST_RF_SIGNAL,
    'msgid': 'testRfSignalTest',
    'nadr': 0,
    'hwpid': 1026,
    'rcode': 0,
    'dpa_value': 35,
    'result': {
        'counter': 131
    },
    'dpa': b'\x00\x00\x02\x8c\x02\x04\x00\x23\x83'
}

data_error: dict = {
    'mtype': OSMessages.TEST_RF_SIGNAL,
    'msgid': 'testRfSignalTest',
    'nadr': 0,
    'hwpid': 1028,
    'rcode': 4,
    'dpa_value': 35,
    'dpa': b'\x00\x00\x02\x8c\x04\x04\x04\x23'
}


class TestRfSignalResponseTestCase(unittest.TestCase):

    @parameterized.expand([
        [
            'from_dpa',
            data_ok,
            ResponseFactory.get_response_from_dpa(data_ok['dpa']),
            False,
        ],
        [
            'from_dpa',
            data_ok_1,
            ResponseFactory.get_response_from_dpa(data_ok_1['dpa']),
            False,
        ],
        [
            'from_json',
            data_ok,
            ResponseFactory.get_response_from_json(generate_json_response(data_ok)),
            True,
        ],
        [
            'from_json',
            data_ok_1,
            ResponseFactory.get_response_from_json(generate_json_response(data_ok_1)),
            True,
        ],
        [
            'from_dpa_error',
            data_error,
            ResponseFactory.get_response_from_dpa(data_error['dpa']),
            False,
        ],
        [
            'from_json_error',
            data_error,
            ResponseFactory.get_response_from_json(generate_json_response(data_error)),
            True,
        ]
    ])
    def test_factory_methods_ok(self, _, response_data, response, json):
        with self.subTest():
            self.assertEqual(response.nadr, response_data['nadr'])
        with self.subTest():
            self.assertEqual(response.pnum, EmbedPeripherals.OS)
        with self.subTest():
            self.assertEqual(response.pcmd, OSResponseCommands.TEST_RF_SIGNAL)
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])
        if json:
            with self.subTest():
                self.assertEqual(response.mtype, OSMessages.TEST_RF_SIGNAL)
            with self.subTest():
                self.assertEqual(response.msgid, response_data['msgid'])

    @parameterized.expand([
        ['from_dpa', data_ok['result']['counter'], TestRfSignalResponse.from_dpa(data_ok['dpa'])],
        ['from_dpa', data_ok_1['result']['counter'], TestRfSignalResponse.from_dpa(data_ok_1['dpa'])],
        ['from_json', data_ok['result']['counter'], TestRfSignalResponse.from_json(generate_json_response(data_ok))],
        ['from_json', data_ok_1['result']['counter'], TestRfSignalResponse.from_json(generate_json_response(data_ok_1))]
    ])
    def test_get_counter(self, _, counter: int, response: TestRfSignalResponse):
        self.assertEqual(response.counter, counter)

    @parameterized.expand([
        ['from_dpa_error', TestRfSignalResponse.from_dpa(data_error['dpa'])],
        ['from_json_error', TestRfSignalResponse.from_json(generate_json_response(data_error))]
    ])
    def test_get_counter_error(self, _, response: TestRfSignalResponse):
        self.assertIsNone(response.counter)

    @parameterized.expand([
        ['from_dpa', '2', TestRfSignalResponse.from_dpa(data_ok['dpa'])],
        ['from_dpa', '0', TestRfSignalResponse.from_dpa(data_ok_1['dpa'])],
        ['from_dpa', '383-510', TestRfSignalResponse.from_dpa(data_ok_2['dpa'])],
        ['from_json', '2', TestRfSignalResponse.from_json(generate_json_response(data_ok))],
        ['from_json', '0', TestRfSignalResponse.from_json(generate_json_response(data_ok_1))],
        ['from_json', '383-510', TestRfSignalResponse.from_json(generate_json_response(data_ok_2))],
    ])
    def test_get_count(self, _, expected: str, response: TestRfSignalResponse):
        self.assertEqual(response.get_count(), expected)

    @parameterized.expand([
        ['from_dpa_error', TestRfSignalResponse.from_dpa(data_error['dpa'])],
        ['from_json_error', TestRfSignalResponse.from_json(generate_json_response(data_error))]
    ])
    def test_get_count_error(self, _, response: TestRfSignalResponse):
        self.assertEqual(response.get_count(), 'None')
