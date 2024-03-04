import unittest
from typing import List, Union
from parameterized import parameterized
from iqrfpy.enums.commands import SensorResponseCommands
from iqrfpy.enums.peripherals import Standards
from iqrfpy.exceptions import DpaResponsePacketLengthError
from iqrfpy.peripherals.sensor.responses.read_sensors import ReadSensorsResponse
from iqrfpy.response_factory import ResponseFactory, SensorReadSensorsFactory

data_ok: dict = {
    'nadr': 2,
    'hwpid': 1026,
    'rcode': 0,
    'dpa_value': 94,
    'dpa': b'\x02\x00\x5e\x80\x02\x04\x00\x5e\x88\x01\x68\x22'
}

data_error: dict = {
    'nadr': 2,
    'hwpid': 1028,
    'rcode': 1,
    'dpa_value': 35,
    'dpa': b'\x02\x00\x5e\x80\x04\x04\x01\x23'
}


class ReadSensorsWithTypesTestCase(unittest.TestCase):

    @parameterized.expand([
        ['from_dpa', data_ok, ResponseFactory.get_response_from_dpa(data_ok['dpa'])],
        ['from_dpa_error', data_error, ResponseFactory.get_response_from_dpa(data_error['dpa'])],
    ])
    def test_factory_methods_ok(self, _, response_data: dict, response: ReadSensorsResponse):
        with self.subTest():
            self.assertEqual(response.nadr, response_data['nadr'])
        with self.subTest():
            self.assertEqual(response.pnum, Standards.SENSOR)
        with self.subTest():
            self.assertEqual(response.pcmd, SensorResponseCommands.READ_SENSORS)
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])

    def test_from_dpa_invalid(self):
        with self.assertRaises(DpaResponsePacketLengthError):
            ReadSensorsResponse.from_dpa(b'\x01\x00\x5e\xbe\x02')

    def test_from_json_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            SensorReadSensorsFactory.create_from_json({})

    @parameterized.expand([
        [
            [136, 1, 104, 34],
            ReadSensorsResponse.from_dpa(data_ok['dpa']),
        ],
    ])
    def test_get_sensor_data(self, values: List[Union[int, float, None]], response: ReadSensorsResponse):
        self.assertEqual(response.sensor_data, values)

    @parameterized.expand([
        ['from_dpa_error', ReadSensorsResponse.from_dpa(data_error['dpa'])],
    ])
    def test_get_sensor_data_error(self, _, response: ReadSensorsResponse):
        self.assertIsNone(response.sensor_data)

