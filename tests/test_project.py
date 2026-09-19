import unittest
from unittest.mock import MagicMock, patch

import requests

import main
import func.function
from func.request import location_check, validate_location_result


class TestProjectFiles(unittest.TestCase):
    def test_main_module_imports(self):
        self.assertIsNotNone(main)

    def test_function_module_imports(self):
        self.assertIsNotNone(func.function)

    @patch("func.request.requests.get")
    def test_location_check_success(self, mock_get):
        ip_response = MagicMock()
        ip_response.raise_for_status.return_value = None
        ip_response.json.return_value = {"ip": "203.0.113.10"}

        geo_response = MagicMock()
        geo_response.raise_for_status.return_value = None
        geo_response.json.return_value = {
            "latitude": 12.345,
            "longitude": 67.890,
            "city": "Sample City",
            "region": "Sample Region",
            "country_name": "Sample Country",
            "postal": "12345",
            "timezone": "UTC",
        }

        mock_get.side_effect = [ip_response, geo_response]

        result = location_check()

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["ip"], "203.0.113.10")
        self.assertEqual(result["city"], "Sample City")
        self.assertEqual(result["location"], (12.345, 67.89))

    @patch(
        "func.request.requests.get",
        side_effect=requests.RequestException("network failed"),
    )
    def test_location_check_handles_network_error(self, _mock_get):
        result = location_check()

        self.assertEqual(result["status"], "error")
        self.assertIn("Network error", result["message"])

    def test_validate_location_result(self):
        valid_result = {
            "status": "success",
            "ip": "203.0.113.10",
            "latitude": 12.345,
            "longitude": 67.89,
            "city": "Sample City",
            "region": "Sample Region",
            "country": "Sample Country",
            "postal_code": "12345",
            "timezone": "UTC",
            "location": (12.345, 67.89),
        }
        invalid_result = {"status": "success", "ip": None, "latitude": "bad"}

        self.assertTrue(validate_location_result(valid_result))
        self.assertFalse(validate_location_result(invalid_result))


if __name__ == "__main__":
    unittest.main()
