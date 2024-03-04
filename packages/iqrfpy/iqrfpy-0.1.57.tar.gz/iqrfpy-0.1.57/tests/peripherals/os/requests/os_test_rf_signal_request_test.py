import unittest
from parameterized import parameterized
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.peripherals.os.requests.test_rf_signal import TestRfSignalRequest


class TestRfSignalTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.default_channel = 25
        self.default_rx_filter = 7
        self.default_time = 10
        self.dpa = b'\x00\x00\x02\x0c\xff\xff\x19\x07\x0a\x00'
        self.json = {
            'mType': 'iqrfEmbedOs_TestRfSignal',
            'data': {
                'msgId': 'testRfSignalTest',
                'req': {
                    'nAdr': 0,
                    'hwpId': 65535,
                    'param': {
                        'channel': self.default_channel,
                        'rxFilter': self.default_rx_filter,
                        'time': self.default_time
                    }
                },
                'returnVerbose': True
            }
        }

    @parameterized.expand([
        [
            25,
            7,
            10,
            b'\x00\x00\x02\x0c\xff\xff\x19\x07\x0a\x00'
        ],
        [
            7,
            5,
            1000,
            b'\x00\x00\x02\x0c\xff\xff\x07\x05\xe8\x03'
        ]
    ])
    def test_to_dpa(self, channel: int, rx_filter: int, time: int, expected: bytes):
        request = TestRfSignalRequest(
            nadr=0,
            channel=channel,
            rx_filter=rx_filter,
            time=time
        )
        self.assertEqual(
            request.to_dpa(),
            expected
        )

    @parameterized.expand([
        [
            25,
            7,
            10,
        ],
        [
            7,
            5,
            1000,
        ]
    ])
    def test_to_json(self, channel: int, rx_filter: int, time: int):
        request = TestRfSignalRequest(
            nadr=0,
            channel=channel,
            rx_filter=rx_filter,
            time=time,
            msgid='testRfSignalTest'
        )
        self.json['data']['req']['param'] = {
            'channel': channel,
            'rxFilter': rx_filter,
            'time': time
        }
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [7],
        [100],
        [255]
    ])
    def test_get_channel(self, channel: int):
        request = TestRfSignalRequest(
            nadr=0,
            channel=self.default_channel,
            rx_filter=self.default_rx_filter,
            time=self.default_time
        )
        self.assertEqual(
            request.channel,
            self.default_channel
        )
        request.channel = channel
        self.assertEqual(
            request.channel,
            channel
        )

    @parameterized.expand([
        [
            10,
            b'\x00\x00\x02\x0c\xff\xff\x0a\x07\x0a\x00'
        ],
        [
            17,
            b'\x00\x00\x02\x0c\xff\xff\x11\x07\x0a\x00'
        ],
        [
            255,
            b'\x00\x00\x02\x0c\xff\xff\xff\x07\x0a\x00'
        ]
    ])
    def test_set_channel(self, channel: int, dpa: bytes):
        request = TestRfSignalRequest(
            nadr=0,
            channel=25,
            rx_filter=7,
            time=10,
            msgid='testRfSignalTest'
        )
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.channel = channel
        self.json['data']['req']['param']['channel'] = channel
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [-1],
        [256],
        [1000],
    ])
    def test_set_channel_invalid(self, channel: int):
        with self.assertRaises(RequestParameterInvalidValueError):
            TestRfSignalRequest(
                nadr=0,
                channel=channel,
                rx_filter=7,
                time=10
            )

    @parameterized.expand([
        [7],
        [100],
        [255]
    ])
    def test_get_rx_filter(self, rx_filter: int):
        request = TestRfSignalRequest(
            nadr=0,
            channel=self.default_channel,
            rx_filter=self.default_rx_filter,
            time=self.default_time
        )
        self.assertEqual(
            request.rx_filter,
            self.default_rx_filter
        )
        request.rx_filter = rx_filter
        self.assertEqual(
            request.rx_filter,
            rx_filter
        )

    @parameterized.expand([
        [
            1,
            b'\x00\x00\x02\x0c\xff\xff\x19\x01\x0a\x00'
        ],
        [
            7,
            b'\x00\x00\x02\x0c\xff\xff\x19\x07\x0a\x00'
        ],
        [
            64,
            b'\x00\x00\x02\x0c\xff\xff\x19\x40\x0a\x00'
        ]
    ])
    def test_set_rx_filter(self, rx_filter: int, dpa: bytes):
        request = TestRfSignalRequest(
            nadr=0,
            channel=25,
            rx_filter=7,
            time=10,
            msgid='testRfSignalTest'
        )
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.rx_filter = rx_filter
        self.json['data']['req']['param']['rxFilter'] = rx_filter
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [-1],
        [256],
        [1000],
    ])
    def test_set_rx_filter_invalid(self, rx_filter: int):
        with self.assertRaises(RequestParameterInvalidValueError):
            TestRfSignalRequest(
                nadr=0,
                channel=25,
                rx_filter=rx_filter,
                time=10
            )

    @parameterized.expand([
        [20],
        [1000],
        [65535]
    ])
    def test_get_time(self, time: int):
        request = TestRfSignalRequest(
            nadr=0,
            channel=self.default_channel,
            rx_filter=self.default_rx_filter,
            time=self.default_time
        )
        self.assertEqual(
            request.time,
            self.default_time
        )
        request.time = time
        self.assertEqual(
            request.time,
            time
        )

    @parameterized.expand([
        [
            10,
            b'\x00\x00\x02\x0c\xff\xff\x19\x07\x0a\x00'
        ],
        [
            100,
            b'\x00\x00\x02\x0c\xff\xff\x19\x07\x64\x00'
        ],
        [
            1000,
            b'\x00\x00\x02\x0c\xff\xff\x19\x07\xe8\x03'
        ]
    ])
    def test_set_time(self, time: int, dpa: bytes):
        request = TestRfSignalRequest(
            nadr=0,
            channel=25,
            rx_filter=7,
            time=10,
            msgid='testRfSignalTest'
        )
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.time = time
        self.json['data']['req']['param']['time'] = time
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [-1],
        [65536],
        [100000],
    ])
    def test_set_time_invalid(self, time: int):
        with self.assertRaises(RequestParameterInvalidValueError):
            TestRfSignalRequest(
                nadr=0,
                channel=25,
                rx_filter=7,
                time=time
            )
