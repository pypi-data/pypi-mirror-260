import unittest

from calculations.utils.common import get_lane_information


class TestGetLaneInformation(unittest.TestCase):
    def test_lane_info(self):
        lane_information = get_lane_information(
            annotations={
                "metrics": {
                    "legData": [
                        {"metadata": {"distance": 50, "strokeType": "Freestyle"}}
                    ]
                },
            },
            relay_leg=None,
        )

        self.assertEqual(
            lane_information,
            {
                "lap_distance": 50,
                "pool_type": "LCM",
                "relay_leg": None,
                "relay_type": "",
                "stroke_type": "Freestyle",
            },
        )

    def test_lane_info_no_metrics(self):
        try:
            get_lane_information(annotations={}, relay_leg=None)
        except Exception as error:
            self.assertEqual(str(error), "There is no metrics data available.")

    def test_lane_info_no_legdata(self):
        try:
            get_lane_information(annotations={"metrics": {}}, relay_leg=None)
        except Exception as error:
            self.assertEqual(str(error), "There is no summary data available.")

    def test_lane_info_empty_legdata(self):
        try:
            get_lane_information(
                annotations={
                    "metrics": {"legData": None},
                },
                relay_leg=None,
            )
        except Exception as error:
            self.assertEqual(str(error), "There is no summary data available.")
