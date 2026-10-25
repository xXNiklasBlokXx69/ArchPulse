import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.report import collect_system_info, save_report


class TestReport(unittest.TestCase):

    def test_collect_system_info(self):
        # Arrange
        with patch("src.report.get_cpu_usage", return_value=25.5), \
             patch("src.report.read_meminfo", return_value=(32.0, 20.0)), \
             patch("src.report.get_disk_usage",
                   return_value=(1000.0, 400.0, 600.0, 40.0)), \
             patch("src.report.get_uptime", return_value=86400.5):

            # Act
            result = collect_system_info()

        # Assert
        expected = {
            "cpu": {
                "usage_percent": 25.5
            },
            "memory": {
                "total_gib": 32.0,
                "available_gib": 20.0,
                "used_gib": 12.0
            },
            "disk": {
                "total_gib": 1000.0,
                "used_gib": 400.0,
                "free_gib": 600.0,
                "usage_percent": 40.0
            },
            "uptime": {
                "seconds": 86400.5
            }
        }

        self.assertEqual(result, expected)

    def test_save_report(self):
        # Arrange
        fake_data = {
            "cpu": {"usage_percent": 25.5},
            "memory": {
                "total_gib": 32.0,
                "available_gib": 20.0,
                "used_gib": 12.0
            },
            "disk": {
                "total_gib": 1000.0,
                "used_gib": 400.0,
                "free_gib": 600.0,
                "usage_percent": 40.0
            },
            "uptime": {"seconds": 86400.5}
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            filename = Path(tmp_dir) / "system.json"

            # Act
            save_report(fake_data, filename)

            # Assert
            self.assertTrue(filename.is_file())

            with open(filename, "r", encoding="utf-8") as f:
                result = json.load(f)

            self.assertEqual(result, fake_data)

    def test_save_report_invalid_path(self):
        # Arrange
        fake_data = {"cpu": {"usage_percent": 25.5}}

        with tempfile.TemporaryDirectory() as tmp_dir:
            filename = Path(tmp_dir) / "nonexistent" / "system.json"

            # Act & Assert
            with self.assertRaises(OSError):
                save_report(fake_data, filename)

    def test_save_report_invalid_data(self):
        # Arrange
        fake_data = {
            "cpu": {"usage_percent": {25.5}}
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            filename = Path(tmp_dir) / "system.json"

            # Act & Assert
            with self.assertRaises(TypeError):
                save_report(fake_data, filename)


if __name__ == "__main__":
    unittest.main()