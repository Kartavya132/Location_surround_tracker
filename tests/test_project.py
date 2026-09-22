import csv
import os
import tempfile
import unittest
from unittest.mock import patch

import func.function
import main
from func.request import calculate_distance_in_meters, save_destination_to_csv


class TestProjectFiles(unittest.TestCase):
    def test_main_module_imports(self):
        self.assertIsNotNone(main)

    def test_function_module_imports(self):
        self.assertIsNotNone(func.function)

    @patch("builtins.input", side_effect=["12.5", "67.8"])
    def test_manual_location_entry(self, _mock_input):
        result = func.function.manual_location_entry()

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["location"], (12.5, 67.8))

    def test_distance_summary_message(self):
        summary = main.build_distance_summary(
            (40.7128, -74.0060),
            (34.0522, -118.2437),
            3940000,
            2000,
        )

        self.assertIn("3940000", summary)
        self.assertIn("2000", summary)

    def test_calculate_distance_in_meters(self):
        current_location = (40.7128, -74.0060)
        destination = (34.0522, -118.2437)

        distance_meters = calculate_distance_in_meters(current_location, destination)

        self.assertAlmostEqual(distance_meters, 3940000, delta=50000)

    def test_save_destination_to_csv(self):
        with tempfile.NamedTemporaryFile("w+", delete=False, newline="") as tmp:
            tmp_path = tmp.name

        try:
            result = save_destination_to_csv(
                (40.7128, -74.0060),
                (34.0522, -118.2437),
                3940000,
                file_path=tmp_path,
            )

            self.assertEqual(result["status"], "success")

            with open(tmp_path, newline="", encoding="utf-8") as csv_file:
                rows = list(csv.DictReader(csv_file))

            self.assertEqual(len(rows), 1)
            self.assertEqual(float(rows[0]["current_latitude"]), 40.7128)
            self.assertEqual(float(rows[0]["destination_latitude"]), 34.0522)
            self.assertEqual(float(rows[0]["distance_meters"]), 3940000)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    @patch("func.function.winsound.Beep")
    def test_check_distance_alarm(self, mock_beep):
        current_location = (40.7128, -74.0060)
        destination = (40.7129, -74.0061)

        result = func.function.check_distance_alarm(current_location, destination, 2000)

        self.assertEqual(result["status"], "success")
        self.assertTrue(result["alarm_triggered"])
        self.assertLess(result["distance_meters"], 2000)
        mock_beep.assert_called()


if __name__ == "__main__":
    unittest.main()
