import unittest
from unittest.mock import mock_open, patch
from io import StringIO

from src.uptime import get_uptime, print_uptime


class TestUptime(unittest.TestCase):

    def test_get_uptime_valid(self):
        # Arrange
        fake_uptime = "192345.67 820456.32"

        # Act
        with patch("builtins.open", mock_open(read_data=fake_uptime)):
            result = get_uptime()

        # Assert
        self.assertAlmostEqual(result, 192345.67, places=2)

    def test_get_uptime_short(self):
        # Arrange
        fake_uptime = "45.50 100.00"

        # Act
        with patch("builtins.open", mock_open(read_data=fake_uptime)):
            result = get_uptime()

        # Assert
        self.assertEqual(result, 45.5)

    def test_get_uptime_zero(self):
        # Arrange
        fake_uptime = "0.00 0.00"

        # Act
        with patch("builtins.open", mock_open(read_data=fake_uptime)):
            result = get_uptime()

        # Assert
        self.assertEqual(result, 0.0)

    def test_get_uptime_invalid(self):
        # Arrange
        fake_uptime = "unknown 100.00"

        # Act & Assert
        with patch("builtins.open", mock_open(read_data=fake_uptime)):
            with self.assertRaises(ValueError):
                get_uptime()

    def test_get_uptime_empty(self):
        # Arrange
        fake_uptime = ""

        # Act & Assert
        with patch("builtins.open", mock_open(read_data=fake_uptime)):
            with self.assertRaises((ValueError, IndexError)):
                get_uptime()

    def test_print_uptime(self):
        # Arrange
        fake_seconds = 192345.67
        expected_output = (
            "System Uptime: 2 days, 5 hours, "
            "25 minutes, 45 seconds\n"
        )

        # Act
        with patch("src.uptime.get_uptime", return_value=fake_seconds):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                print_uptime()

        # Assert
        self.assertEqual(mock_stdout.getvalue(), expected_output)


if __name__ == "__main__":
    unittest.main()