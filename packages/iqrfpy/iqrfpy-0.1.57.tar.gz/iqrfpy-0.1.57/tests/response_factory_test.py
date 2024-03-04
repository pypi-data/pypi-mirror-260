import unittest

from parameterized import parameterized

from iqrfpy.async_response import AsyncResponse
from iqrfpy.confirmation import Confirmation
from iqrfpy.exceptions import JsonMsgidMissingError, JsonMTypeMissingError, UnsupportedMessageTypeError, \
    UnsupportedPeripheralError, UnsupportedPeripheralCommandError
from iqrfpy.peripherals.coordinator.responses import *
from iqrfpy.response_factory import *


class ResponseFactoryTestCase(unittest.TestCase):

    @parameterized.expand([
        ['Async', b'\x00\x00\xff\x3f\x00\x00\x80\x00\x17\x04\x00\xfd\x26\x00\x00\x00\x00\x00\x00\x05', AsyncResponse],
        ['Confirmation', b'\x01\x00\x01\x00\xff\xff\xff\x36\x01\x04\x01', Confirmation],
        ['AddrInfo', b'\x00\x00\x00\x80\x00\x00\x00\x40\x0a\x2a', AddrInfoResponse],
        ['ClearAllBonds', b'\x00\x00\x00\x83\x00\x00\x00\x40', ClearAllBondsResponse],
        ['SmartConnect', b'\x00\x00\x00\x92\x00\x00\x00\x47\x01\x02', SmartConnectResponse]
    ])
    def test_response_from_dpa_ok(self, _, dpa, expected):
        self.assertIsInstance(ResponseFactory.get_response_from_dpa(dpa=dpa), expected)

    @parameterized.expand([
        ['Nonsense', b'\x0b\x0a']
    ])
    def test_response_from_dpa_invalid(self, _, dpa):
        with self.assertRaises(ValueError):
            ResponseFactory.get_response_from_dpa(dpa=dpa)

    @parameterized.expand([
        ['Async', {
            'mType': 'iqrfRaw',
            'data': {
                'msgId': 'async',
                'rsp': {
                    'rData': '00.00.ff.3f.00.00.80.00.17.04.00.fd.26.00.00.00.00.00.00.05'
                },
                'status': 0,
                'insId': 'iqrfgd2-default'
            }
        }, AsyncResponse],
        ['BondNode', {
            "mType": "iqrfEmbedCoordinator_BondNode",
            "data": {
                "msgId": "testEmbedCoordinator",
                "rsp": {
                    "nAdr": 0,
                    "hwpId": 0,
                    "rCode": 0,
                    "dpaVal": 53,
                    "result": {
                        "bondAddr": 1,
                        "devNr": 2
                    }
                },
                "insId": "iqrfgd2-1",
                "status": 0
            }
        }, BondNodeResponse],
        ['RemoveBond', {
            "mType": "iqrfEmbedCoordinator_RemoveBond",
            "data": {
                "msgId": "testEmbedCoordinator",
                "rsp": {
                    "nAdr": 0,
                    "hwpId": 0,
                    "rCode": 0,
                    "dpaVal": 53,
                    "result": {
                        "devNr": 1
                    }
                },
                "insId": "iqrfgd2-1",
                "status": 0
            }
        }, RemoveBondResponse],
        ['SetHops', {
            "mType": "iqrfEmbedCoordinator_SetHops",
            "data": {
                "msgId": "testEmbedCoordinator",
                "rsp": {
                    "nAdr": 0,
                    "hwpId": 0,
                    "rCode": 0,
                    "dpaVal": 0,
                    "result": {
                        "requestHops": 255,
                        "responseHops": 255
                    }
                },
                "insId": "iqrfgd2-1",
                "status": 0
            }
        }, SetHopsResponse]
    ])
    def test_response_from_json_ok(self, _, json, expected):
        self.assertIsInstance(ResponseFactory.get_response_from_json(json=json), expected)

    @parameterized.expand([
        [{'data': {'req': {}}}, JsonMsgidMissingError],
        [{'data': {'msgId': 'test'}}, JsonMTypeMissingError],
        [{'mType': 'unsupported', 'data': {'msgId': 'test'}}, UnsupportedMessageTypeError],
    ])
    def test_response_from_json_invalid(self, json, exception):
        with self.assertRaises(exception):
            ResponseFactory.get_response_from_json(json=json)

    @parameterized.expand([
        [
            'unknown_peripheral',
            111,
            133,
        ],
        [
            'unknown_command',
            10,
            133,
        ],
    ])
    def test_get_factory_from_dpa_generic(self, _, pnum: int, pcmd: int):
        try:
            ResponseFactory.get_factory_from_dpa(pnum, pcmd, True)
        except UnsupportedPeripheralError | UnsupportedPeripheralCommandError:
            self.fail('Exception raised, should not have been raised.')

    @parameterized.expand([
        [
            'unknown_peripheral',
            111,
            133,
            UnsupportedPeripheralError,
        ],
        [
            'unknown_command',
            10,
            133,
            UnsupportedPeripheralCommandError
        ],
    ])
    def test_get_factory_from_dpa_unknown(self, _, pnum: int, pcmd: int, exception):
        with self.assertRaises(exception):
            ResponseFactory.get_factory_from_dpa(pnum, pcmd)

    def test_get_response_from_dpa_unknown(self):
        with self.subTest():
            with self.assertRaises(UnsupportedPeripheralError):
                ResponseFactory.get_response_from_dpa(b'\x00\x00\x6f\x85\xff\xff\x00\x35')
        with self.subTest():
            with self.assertRaises(UnsupportedPeripheralCommandError):
                ResponseFactory.get_response_from_dpa(b'\x00\x00\x0a\x85\xff\xff\x00\x35')

    def test_get_factory_from_mtype_unknown(self):
        with self.assertRaises(UnsupportedMessageTypeError):
            ResponseFactory.get_factory_from_mtype('unknown')
