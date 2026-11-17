"""Wearable locate results (cptLocateInfoList) parsing tests."""

import json
import unittest

from custom_components.huawei_find.api import _parse_locate_info


def _payload(coords):
    return {
        "locateInfo": "",
        "cptLocateInfoList": [
            {
                "batteryStatus": json.dumps({"percentage": "81"}),
                "coordinateInfoList": coords,
            }
        ],
    }


class CptParseTests(unittest.TestCase):
    def test_prefers_wgs84_entry(self):
        payload = _payload(
            [
                json.dumps({"latitude": 31.329087, "longitude": 120.441357, "sysType": "2", "accuracy": "17.2"}),
                json.dumps({"latitude": 31.3251733, "longitude": 120.4301412, "sysType": "1", "accuracy": "17.2"}),
            ]
        )
        result = _parse_locate_info(payload)
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result["latitude"], 31.3251733, places=5)
        self.assertAlmostEqual(result["longitude"], 120.4301412, places=5)
        self.assertEqual(result["coordinate_system"], "wgs84")
        self.assertEqual(result["battery"], 81)

    def test_converts_bd09_when_only_bd09(self):
        payload = _payload(
            [json.dumps({"latitude": 31.329087, "longitude": 120.441357, "sysType": "2"})]
        )
        result = _parse_locate_info(payload)
        self.assertIsNotNone(result)
        self.assertEqual(result["coordinate_system"], "bd09")
        self.assertAlmostEqual(result["latitude"], 31.3251733, places=3)
        self.assertAlmostEqual(result["longitude"], 120.4301412, places=3)

    def test_empty_payload(self):
        self.assertIsNone(_parse_locate_info({"locateInfo": ""}))
        self.assertIsNone(_parse_locate_info({}))


if __name__ == "__main__":
    unittest.main()
