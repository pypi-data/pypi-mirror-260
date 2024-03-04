import unittest
from iqrfpy.peripherals.os.requests.factory_settings import FactorySettingsRequest


class FactorySettingsRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.request = FactorySettingsRequest(nadr=2, msgid='factorySettingsTest')
        self.dpa = b'\x02\x00\x02\x0d\xff\xff'
        self.json = {
            'mType': 'iqrfEmbedOs_FactorySettings',
            'data': {
                'msgId': 'factorySettingsTest',
                'req': {
                    'nAdr': 2,
                    'hwpId': 65535,
                    'param': {},
                },
                'returnVerbose': True
            },
        }

    def test_to_dpa(self):
        self.assertEqual(
            self.request.to_dpa(),
            self.dpa
        )

    def test_to_json(self):
        self.assertEqual(
            self.request.to_json(),
            self.json
        )
