import unittest
from parameterized import parameterized
from iqrfpy.enums.commands import OSResponseCommands
from iqrfpy.enums.message_types import OSMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.peripherals.os.responses.load_code import LoadCodeResponse
from tests.helpers.json import generate_json_response
from iqrfpy.response_factory import ResponseFactory
from iqrfpy.utils.dpa import OsLoadCodeErrors, OsLoadCodeResult

data_ok: dict = {
    'mtype': OSMessages.LOAD_CODE,
    'msgid': 'loadCodeTest',
    'nadr': 0,
    'hwpid': 0,
    'rcode': 0,
    'dpa_value': 90,
    'result': {
        'loadingCode': 0
    },
    'dpa': b'\x00\x00\x02\x8a\x00\x00\x00\x5a\x00'
}

data_ok_1: dict = {
    'mtype': OSMessages.LOAD_CODE,
    'msgid': 'loadCodeTest',
    'nadr': 0,
    'hwpid': 1026,
    'rcode': 0,
    'dpa_value': 35,
    'result': {
        'loadingCode': 1
    },
    'dpa': b'\x00\x00\x02\x8a\x02\x04\x00\x23\x01'
}

data_ok_2: dict = {
    'mtype': OSMessages.LOAD_CODE,
    'msgid': 'loadCodeTest',
    'nadr': 0,
    'hwpid': 0,
    'rcode': 0,
    'dpa_value': 90,
    'result': {
        'loadingCode': 8
    },
    'dpa': b'\x00\x00\x02\x8a\x00\x00\x00\x5a\x08'
}
data_ok_3: dict = {
    'mtype': OSMessages.LOAD_CODE,
    'msgid': 'loadCodeTest',
    'nadr': 0,
    'hwpid': 0,
    'rcode': 0,
    'dpa_value': 90,
    'result': {
        'loadingCode': 20
    },
    'dpa': b'\x00\x00\x02\x8a\x00\x00\x00\x5a\x14'
}

data_error: dict = {
    'mtype': OSMessages.LOAD_CODE,
    'msgid': 'loadCodeTest',
    'nadr': 0,
    'hwpid': 1028,
    'rcode': 4,
    'dpa_value': 35,
    'dpa': b'\x00\x00\x02\x8a\x04\x04\x04\x23'
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
            self.assertEqual(response.pcmd, OSResponseCommands.LOAD_CODE)
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])
        if json:
            with self.subTest():
                self.assertEqual(response.mtype, OSMessages.LOAD_CODE)
            with self.subTest():
                self.assertEqual(response.msgid, response_data['msgid'])

    @parameterized.expand([
        ['from_dpa', data_ok['result']['loadingCode'], LoadCodeResponse.from_dpa(data_ok['dpa'])],
        ['from_dpa', data_ok_1['result']['loadingCode'], LoadCodeResponse.from_dpa(data_ok_1['dpa'])],
        ['from_json', data_ok['result']['loadingCode'], LoadCodeResponse.from_json(generate_json_response(data_ok))],
        ['from_json', data_ok_1['result']['loadingCode'], LoadCodeResponse.from_json(generate_json_response(data_ok_1))]
    ])
    def test_get_load_result(self, _, load_result: int, response: LoadCodeResponse):
        self.assertEqual(response.load_result, load_result)

    @parameterized.expand([
        ['from_dpa_error', LoadCodeResponse.from_dpa(data_error['dpa'])],
        ['from_json_error', LoadCodeResponse.from_json(generate_json_response(data_error))]
    ])
    def test_get_load_result_no_response(self, _, response: LoadCodeResponse):
        self.assertIsNone(response.load_result)

    @parameterized.expand([
        ['from_dpa', OsLoadCodeResult.ERROR, LoadCodeResponse.from_dpa(data_ok['dpa'])],
        ['from_dpa', OsLoadCodeResult.NO_ERROR, LoadCodeResponse.from_dpa(data_ok_1['dpa'])],
        ['from_json', OsLoadCodeResult.ERROR, LoadCodeResponse.from_json(generate_json_response(data_ok))],
        ['from_json', OsLoadCodeResult.NO_ERROR, LoadCodeResponse.from_json(generate_json_response(data_ok_1))]
    ])
    def test_get_load_result_parsed(self, _, result: OsLoadCodeResult, response: LoadCodeResponse):
        self.assertEqual(response.get_load_result(), result)

    @parameterized.expand([
        ['from_dpa_error', LoadCodeResponse.from_dpa(data_error['dpa'])],
        ['from_json_error', LoadCodeResponse.from_json(generate_json_response(data_error))]
    ])
    def test_get_load_result_parsed_no_response(self, _, response: LoadCodeResponse):
        self.assertIsNone(response.get_load_result())

    @parameterized.expand([
        ['from_dpa', OsLoadCodeErrors.HEX_IQRF_CHECKSUM_MISMATCH, LoadCodeResponse.from_dpa(data_ok['dpa'])],
        ['from_dpa', OsLoadCodeErrors.IQRF_OS_CHANGE_CHECKSUM_MISMATCH, LoadCodeResponse.from_dpa(data_ok_2['dpa'])],
        ['from_dpa', OsLoadCodeErrors.RESERVED, LoadCodeResponse.from_dpa(data_ok_3['dpa'])],
        ['from_json', OsLoadCodeErrors.HEX_IQRF_CHECKSUM_MISMATCH, LoadCodeResponse.from_json(generate_json_response(data_ok))],
        ['from_json', OsLoadCodeErrors.IQRF_OS_CHANGE_CHECKSUM_MISMATCH, LoadCodeResponse.from_json(generate_json_response(data_ok_2))],
        ['from_json', OsLoadCodeErrors.RESERVED, LoadCodeResponse.from_json(generate_json_response(data_ok_3))]
    ])
    def test_get_load_error(self, _, result: OsLoadCodeErrors, response: LoadCodeResponse):
        self.assertEqual(response.get_load_error(), result)

    @parameterized.expand([
        ['from_dpa_error', LoadCodeResponse.from_dpa(data_error['dpa'])],
        ['from_json_error', LoadCodeResponse.from_json(generate_json_response(data_error))]
    ])
    def test_get_load_error_no_response(self, _, response: LoadCodeResponse):
        self.assertIsNone(response.get_load_error())
