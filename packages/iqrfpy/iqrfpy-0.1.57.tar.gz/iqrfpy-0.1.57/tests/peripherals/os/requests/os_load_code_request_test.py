import unittest
from typing import Union

from parameterized import parameterized
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.peripherals.os.requests.load_code import LoadCodeRequest, OsLoadCodeFlags
from iqrfpy.utils.dpa import OsLoadCodeAction, OsLoadCodeType


class LoadCodeRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.default_flags = 0
        self.default_address = 0
        self.default_length = 64
        self.default_checksum = 59962
        self.dpa = b'\x01\x00\x02\x0a\xff\xff\x00\x00\x00\x40\x00\x3a\xea'
        self.json = {
            'mType': 'iqrfEmbedOs_LoadCode',
            'data': {
                'msgId': 'loadCodeTest',
                'req': {
                    'nAdr': 1,
                    'hwpId': 65535,
                    'param': {
                        'flags': 0,
                        'address': 0,
                        'length': 64,
                        'checkSum': 59962,
                    }
                },
                'returnVerbose': True
            }
        }

    @parameterized.expand([
        [
            'integer_flags',
            1,
            10,
            64,
            48161,
            b'\x01\x00\x02\x0a\xff\xff\x01\x0a\x00\x40\x00\x21\xbc',
        ],
        [
            'class_flags',
            OsLoadCodeFlags(action=OsLoadCodeAction.VERIFY_AND_LOAD, code_type=OsLoadCodeType.CUSTOM_DPA_HANDLER),
            10,
            64,
            48161,
            b'\x01\x00\x02\x0a\xff\xff\x01\x0a\x00\x40\x00\x21\xbc',
        ]
    ])
    def test_to_dpa(self, _, flags: Union[OsLoadCodeFlags, int], address: int, length: int, checksum: int, expected: bytes):
        request = LoadCodeRequest(
            nadr=1,
            flags=flags,
            address=address,
            length=length,
            checksum=checksum
        )
        self.assertEqual(
            request.to_dpa(),
            expected
        )

    @parameterized.expand([
        [
            'integer_flags',
            1,
            10,
            64,
            48161,
        ],
        [
            'class_flags',
            OsLoadCodeFlags(action=OsLoadCodeAction.VERIFY_AND_LOAD, code_type=OsLoadCodeType.CUSTOM_DPA_HANDLER),
            10,
            64,
            48161,
        ]
    ])
    def test_to_json(self, _, flags: Union[OsLoadCodeFlags, int], address: int, length: int, checksum: int):
        request = LoadCodeRequest(
            nadr=1,
            flags=flags,
            address=address,
            length=length,
            checksum=checksum,
            msgid='loadCodeTest',
        )
        self.json['data']['req']['param'] = {
            'flags': flags.serialize() if isinstance(flags, OsLoadCodeFlags) else flags,
            'address': address,
            'length': length,
            'checkSum': checksum,
        }
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [2],
        [OsLoadCodeFlags(action=OsLoadCodeAction.VERIFY, code_type=OsLoadCodeType.IQRF_PLUGIN)],
    ])
    def test_get_flags(self, flags: Union[OsLoadCodeFlags, int]):
        request = LoadCodeRequest(
            nadr=1,
            flags=self.default_flags,
            address=self.default_address,
            length=self.default_length,
            checksum=self.default_checksum,
        )
        self.assertEqual(
            request.flags,
            self.default_flags
        )
        request.flags = flags
        self.assertEqual(
            request.flags,
            flags
        )

    @parameterized.expand([
        [
            'integer_flags',
            5,
            b'\x01\x00\x02\x0a\xff\xff\x05\x00\x00\x40\x00\x3a\xea',
        ],
        [
            'class_flags',
            OsLoadCodeFlags(action=OsLoadCodeAction.VERIFY_AND_LOAD, code_type=OsLoadCodeType.IQRF_OS_CHANGE_FILE),
            b'\x01\x00\x02\x0a\xff\xff\x05\x00\x00\x40\x00\x3a\xea'
        ],
        [
            'integer_flags',
            3,
            b'\x01\x00\x02\x0a\xff\xff\x03\x00\x00\x40\x00\x3a\xea',
        ],
        [
            'class_flags',
            OsLoadCodeFlags(action=OsLoadCodeAction.VERIFY_AND_LOAD, code_type=OsLoadCodeType.IQRF_PLUGIN),
            b'\x01\x00\x02\x0a\xff\xff\x03\x00\x00\x40\x00\x3a\xea'
        ]
    ])
    def test_set_flags(self, _, flags: Union[OsLoadCodeFlags, int], dpa: bytes):
        request = LoadCodeRequest(
            nadr=1,
            flags=self.default_flags,
            address=self.default_address,
            length=self.default_length,
            checksum=self.default_checksum,
            msgid='loadCodeTest',
        )
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.flags = flags
        self.json['data']['req']['param']['flags'] = flags.serialize() if isinstance(flags, OsLoadCodeFlags) else flags
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
    def test_set_flags_invalid(self, flags: Union[OsLoadCodeFlags, int]):
        with self.assertRaises(RequestParameterInvalidValueError):
            LoadCodeRequest(
                nadr=1,
                flags=flags,
                address=self.default_address,
                length=self.default_length,
                checksum=self.default_checksum,
            )

    @parameterized.expand([
        [2],
        [100],
        [1000],
        [65535],
    ])
    def test_get_address(self, address: int):
        request = LoadCodeRequest(
            nadr=1,
            flags=self.default_flags,
            address=self.default_address,
            length=self.default_length,
            checksum=self.default_checksum,
        )
        self.assertEqual(
            request.address,
            self.default_address
        )
        request.address = address
        self.assertEqual(
            request.address,
            address
        )

    @parameterized.expand([
        [
            2,
            b'\x01\x00\x02\x0a\xff\xff\x00\x02\x00\x40\x00\x3a\xea',
        ],
        [
            100,
            b'\x01\x00\x02\x0a\xff\xff\x00\x64\x00\x40\x00\x3a\xea'
        ],
        [
            1000,
            b'\x01\x00\x02\x0a\xff\xff\x00\xe8\x03\x40\x00\x3a\xea',
        ],
        [
            65535,
            b'\x01\x00\x02\x0a\xff\xff\x00\xff\xff\x40\x00\x3a\xea'
        ]
    ])
    def test_set_address(self, address: int, dpa: bytes):
        request = LoadCodeRequest(
            nadr=1,
            flags=self.default_flags,
            address=self.default_address,
            length=self.default_length,
            checksum=self.default_checksum,
            msgid='loadCodeTest',
        )
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.address = address
        self.json['data']['req']['param']['address'] = address
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
    def test_set_address_invalid(self, address: int):
        with self.assertRaises(RequestParameterInvalidValueError):
            LoadCodeRequest(
                nadr=1,
                flags=self.default_flags,
                address=address,
                length=self.default_length,
                checksum=self.default_checksum
            )

    @parameterized.expand([
        [2],
        [100],
        [1000],
        [65535],
    ])
    def test_get_length(self, length: int):
        request = LoadCodeRequest(
            nadr=1,
            flags=self.default_flags,
            address=self.default_address,
            length=self.default_length,
            checksum=self.default_checksum,
        )
        self.assertEqual(
            request.length,
            self.default_length
        )
        request.length = length
        self.assertEqual(
            request.length,
            length
        )

    @parameterized.expand([
        [
            2,
            b'\x01\x00\x02\x0a\xff\xff\x00\x00\x00\x02\x00\x3a\xea',
        ],
        [
            100,
            b'\x01\x00\x02\x0a\xff\xff\x00\x00\x00\x64\x00\x3a\xea'
        ],
        [
            1000,
            b'\x01\x00\x02\x0a\xff\xff\x00\x00\x00\xe8\x03\x3a\xea',
        ],
        [
            65535,
            b'\x01\x00\x02\x0a\xff\xff\x00\x00\x00\xff\xff\x3a\xea'
        ]
    ])
    def test_set_length(self, length: int, dpa: bytes):
        request = LoadCodeRequest(
            nadr=1,
            flags=self.default_flags,
            address=self.default_address,
            length=self.default_length,
            checksum=self.default_checksum,
            msgid='loadCodeTest',
        )
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.length = length
        self.json['data']['req']['param']['length'] = length
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
    def test_set_length_invalid(self, length: int):
        with self.assertRaises(RequestParameterInvalidValueError):
            LoadCodeRequest(
                nadr=1,
                flags=self.default_flags,
                address=self.default_address,
                length=length,
                checksum=self.default_checksum
            )

    @parameterized.expand([
        [2],
        [100],
        [1000],
        [65535],
    ])
    def test_get_checksum(self, checksum: int):
        request = LoadCodeRequest(
            nadr=1,
            flags=self.default_flags,
            address=self.default_address,
            length=self.default_length,
            checksum=self.default_checksum,
        )
        self.assertEqual(
            request.checksum,
            self.default_checksum
        )
        request.checksum = checksum
        self.assertEqual(
            request.checksum,
            checksum
        )

    @parameterized.expand([
        [
            2,
            b'\x01\x00\x02\x0a\xff\xff\x00\x00\x00\x40\x00\x02\x00',
        ],
        [
            100,
            b'\x01\x00\x02\x0a\xff\xff\x00\x00\x00\x40\x00\x64\x00'
        ],
        [
            1000,
            b'\x01\x00\x02\x0a\xff\xff\x00\x00\x00\x40\x00\xe8\x03',
        ],
        [
            65535,
            b'\x01\x00\x02\x0a\xff\xff\x00\x00\x00\x40\x00\xff\xff'
        ]
    ])
    def test_set_checksum(self, checksum: int, dpa: bytes):
        request = LoadCodeRequest(
            nadr=1,
            flags=self.default_flags,
            address=self.default_address,
            length=self.default_length,
            checksum=self.default_checksum,
            msgid='loadCodeTest',
        )
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.checksum = checksum
        self.json['data']['req']['param']['checkSum'] = checksum
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
    def test_set_checksum_invalid(self, checksum: int):
        with self.assertRaises(RequestParameterInvalidValueError):
            LoadCodeRequest(
                nadr=1,
                flags=self.default_flags,
                address=self.default_address,
                length=self.default_length,
                checksum=checksum
            )
